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
    else:
        return (
            scale["8_person_household"]
            + ((household_size - 8) * (scale['additional_per_person_above_8']))
            )


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
            family('homelessness', period)
            + family('fostercare', period)
            + family('eligible_tanf_or_ssi', period)
            + family('below_federal_poverty_level', period)
            )
