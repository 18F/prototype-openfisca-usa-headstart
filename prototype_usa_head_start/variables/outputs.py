# -*- coding: utf-8 -*-

# This file defines variables for the rules.
# See https://openfisca.org/doc/key-concepts/variables.html.

from openfisca_core.model_api import *
from prototype_usa_head_start.entities import *
import numpy as np


def household_to_cutoff_value(household_size_and_fpl_scale):
    household_size = household_size_and_fpl_scale[0]
    scale = household_size_and_fpl_scale[1]

    if (0 < household_size < 9):
        return scale[str(household_size) + "_person_household"]
    elif (9 <= household_size):
        return (
            scale["8_person_household"]
            + ((household_size - 8) * (scale['additional_per_person_above_8']))
            )
    elif (household_size <= 0):
        raise ValueError('Household size out of bounds (at or below zero).')


class federal_poverty_line_value(Variable):
    value_type = int
    entity = Family
    definition_period = YEAR
    label = u"What is the federal poverty line cutoff for a family based on their state of residence and their household size?"

    def formula(family, period, parameters):
        state_or_territory = family('state_or_territory', period)
        federal_poverty_levels = parameters(period).federal_poverty_level

        ak_poverty_levels = federal_poverty_levels['AK']
        hi_poverty_levels = federal_poverty_levels['HI']
        default_poverty_levels = federal_poverty_levels['DEFAULT']

        federal_poverty_line_scale = select(
            [state_or_territory == 'AK', state_or_territory == 'HI'],
            [ak_poverty_levels, hi_poverty_levels],
            default_poverty_levels
            )

        household_size = family('household_size', period)

        household_size_and_fpl_scale = np.column_stack((household_size, federal_poverty_line_scale))

        return list(map(
                    household_to_cutoff_value,
                    household_size_and_fpl_scale
                    ))


class equal_to_or_below_federal_poverty_level(Variable):
    value_type = bool
    entity = Family
    definition_period = YEAR
    label = u"Is the family's income below the federal poverty level?"
    # From the policy:
    # "Eligibility requirements. (1) A pregnant woman or a child is eligible if: (i) The family’s income is equal to or below the poverty line...""
    # SOURCE: https://eclkc.ohs.acf.hhs.gov/policy/45-cfr-chap-xiii/1302-12-determining-verifying-documenting-eligibility

    def formula(family, period, parameters):
        return (
            family('federal_poverty_line_value', period) >= family('income', period)
            )


class income_between_fpl_and_130_fpl(Variable):
    value_type = bool
    entity = Family
    definition_period = YEAR
    label = u"Is the family's income below 130 percent of the federal poverty level?"
    # From the policy:
    # If a program chooses to enroll participants who do not meet a criterion in paragraph (c) of this section, and whose family incomes are between 100 and 130 percent of the poverty line, ...
    # TODO (ARS): Check the below with Head Start.
    # NOTE (ARS): Since the eligibility rules reference "equal to or below the poverty line" for purposes of determining eligibility, I interpret "between 100 and 130 percent" to be inclusive of 130 percent.
    # SOURCE: https://eclkc.ohs.acf.hhs.gov/policy/45-cfr-chap-xiii/1302-12-determining-verifying-documenting-eligibility

    def formula(family, period, parameters):
        return (
            (family('federal_poverty_line_value', period) * 1.3) >= family('income', period) > family('federal_poverty_line_value', period)
            )


class head_start_eligibility_bool(Variable):
    value_type = bool
    entity = Family
    definition_period = YEAR
    label = u"Head Start Eligibility Boolean"

    def formula(family, period, parameters):
        return (
            family('homelessness', period)
            + family('fostercare', period)
            + family('eligible_tanf_or_ssi', period)
            + family('equal_to_or_below_federal_poverty_level', period)
            )


def add_eligibility_reason(current_string, bool_series, statement):
    return concat(current_string, where(bool_series, statement, ''))


class head_start_eligibility_status(Variable):
    value_type = str
    entity = Family
    definition_period = YEAR
    label = u"Head Start Eligibility Status"

    def formula(family, period, parameters):
        # TODO (ARS): Check with Head Start about whether the API should return
        # may be status or eligible status for child with a disability.
        # TODO (ARS): Same with ([100% FPL] < income =< [130% FPL]).
        eligible_status = 'Eligible for Head Start. Slot in a program not guaranteed.'
        maybe_status = 'May be Eligible, depending on the child\'s needs and the slots available.'
        eligibility_boolean = family('head_start_eligibility_bool', period)

        determination = where(eligibility_boolean, eligible_status, maybe_status)

        with_homelessness_factor = add_eligibility_reason(
            determination,
            family('homelessness', period),
            ' Eligible because the family is experiencing homelessness.'
            )

        with_fostercare_factor = add_eligibility_reason(
            with_homelessness_factor,
            family('fostercare', period),
            ' Eligible because the child is in foster care.'
            )

        with_tanf_ssi_factor = add_eligibility_reason(
            with_fostercare_factor,
            family('eligible_tanf_or_ssi', period),
            ' Eligible because of eligibility for TANF or SSI.'
            )

        with_poverty_line_factor = add_eligibility_reason(
            with_tanf_ssi_factor,
            family('equal_to_or_below_federal_poverty_level', period),
            ' Eligible because family is below the federal poverty line.'
            )

        with_disability_factor = add_eligibility_reason(
            with_poverty_line_factor,
            family('disability', period),
            # TODO (ARS): Check language with Head Start counterparts.
            ' May be eligible due to the child\'s disability. Head Start programs must fill 10 percent of slots with children covered by the Individuals with Disabilities Education Act.'
            )

        with_130_fpl_factor = add_eligibility_reason(
            with_disability_factor,
            family('income_between_fpl_and_130_fpl', period),
            # TODO (ARS): Check language with Head Start counterparts.
            ' May be eligible because family income is equal to or below 130 percent of the federal poverty level. Some Head Start programs have additional capacity for families with income in this range.'
            )

        result = with_130_fpl_factor

        return result
