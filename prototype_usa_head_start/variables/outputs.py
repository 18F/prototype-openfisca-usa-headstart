# -*- coding: utf-8 -*-

# This file defines variables for the rules.
# See https://openfisca.org/doc/key-concepts/variables.html.

from openfisca_core.model_api import *
from prototype_usa_head_start.entities import *


class federal_poverty_line_value(Variable):
    value_type = bool
    entity = Family
    definition_period = YEAR
    label = u"What is the federal poverty line cutoff for a family based on their state of residence and their household size?"

    def formula(family, period, parameters):
        household_size = family('household_size', period)
        state_or_territory = family('state_or_territory', period)
        federal_poverty_levels = parameters(period).federal_poverty_level
        ak_poverty_levels = federal_poverty_levels['AK']
        hi_poverty_levels = federal_poverty_levels['HI']
        default_poverty_levels = federal_poverty_levels['DEFAULT']

        by_state_poverty_levels = select(
            [state_or_territory == 'AK', state_or_territory == 'HI'],
            [ak_poverty_levels, hi_poverty_levels],
            default_poverty_levels
            )

        by_household_size_key = concat(household_size, '_person_household')

        ## TODO: Make this work
        print('by_household_size_key')
        print(by_household_size_key)
        return False

        # if (9 > household_size):
        #     household_size_key = str(household_size[0]) + "_person_household"
        #     cutoff_value = local_guidelines[household_size_key]
        # else:
        #     eight_person_cutoff = local_guidelines["8_person_household"]
        #     additional_per_person = local_guidelines["additional_per_person_above_8"]
        #     people_above_8 = household_size - 8
        #     cutoff_value = eight_person_cutoff + (additional_per_person * people_above_8)


class below_federal_poverty_level(Variable):
    value_type = bool
    entity = Family
    definition_period = YEAR
    label = u"Is the family below the federal poverty level?"

    def formula(family, period, parameters):
        return (
            family('federal_poverty_line_value', period) > family('income', period)
            )


class head_start_eligibility_status(Variable):
    value_type = bool
    entity = Family
    definition_period = YEAR
    label = u"Head Start Eligibility Status"

    def formula(family, period, parameters):
        return (
            + family('homelessness', period)
            + family('fostercare', period)
            + family('eligible_tanf_or_ssi', period)
            + family('below_federal_poverty_level', period)
            )
