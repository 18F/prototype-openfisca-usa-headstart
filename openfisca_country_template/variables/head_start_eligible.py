# -*- coding: utf-8 -*-

# This file defines variables for the rules.
# See https://openfisca.org/doc/key-concepts/variables.html.

from openfisca_core.model_api import *
from openfisca_country_template.entities import *


class eligible(Variable):
    value_type = bool
    entity = Family
    definition_period = YEAR
    label = "Eligible for Head Start"

    def formula(family, period):
        homelessness = family('homelessness', period)
        fostercare = family('fostercare', period)
        eligible_tanf_or_ssi = family('eligible_tanf_or_ssi', period)

        # TODO: Get Head Start input on this "early return" strategy
        if (homelessness or fostercare or eligible_tanf_or_ssi):
            return True

        income = family('income', period)
        household_size = family('household_size', period)
        state_or_territory = family('state_or_territory', period)

        # These should be expressed as parameters, but I'm having issues getting my parameters YAML to load correctly. Expressing here as JSON for now.
        federal_poverty_level_data = {"federal_poverty_level": {"2019-01-11": {"AK": {"1_person_household": {"value": 15600}, "2_person_household": {"value": 21130}, "3_person_household": {"value": 26660}, "4_person_household": {"value": 32190}, "5_person_household": {"value": 37720}, "6_person_household": {"value": 43250}, "7_person_household": {"value": 48780}, "8_person_household": {"value": 54310}, "additional_per_person_above_8": {"value": 5530}}, "forty_eight_states_plus_dc": {"1_person_household": {"value": 12490}, "2_person_household": {"value": 16910}, "3_person_household": {"value": 21330}, "4_person_household": {"value": 25750}, "5_person_household": {"value": 30170}, "6_person_household": {"value": 34590}, "7_person_household": {"value": 39010}, "8_person_household": {"value": 43430}, "additional_per_person_above_8": {"value": 4420}}, "HI": {"1_person_household": {"value": 14380}, "2_person_household": {"value": 19460}, "3_person_household": {"value": 24540}, "4_person_household": {"value": 29620}, "5_person_household": {"value": 34700}, "6_person_household": {"value": 39780}, "7_person_household": {"value": 44860}, "8_person_household": {"value": 49940}, "additional_per_person_above_8": {"value": 5080}}}}}

        fpl_guidelines = federal_poverty_level_data.get('federal_poverty_level').get('2019-01-11')

        if ((state_or_territory == 'AK') or (state_or_territory == 'HI')):
            local_guidelines = fpl_guidelines.get(state_or_territory)
        else:
            local_guidelines = fpl_guidelines.get('forty_eight_states_plus_dc')

        if (9 > household_size):
            household_size_key = str(household_size[0]) + "_person_household"
            cutoff_value = local_guidelines.get(household_size_key).get('value')
        else:
            eight_person_cutoff = local_guidelines.get("8_person_household").get('value')
            additional_per_person = local_guidelines.get("additional_per_person_above_8").get('value')
            people_above_8 = household_size - 8
            cutoff_value = eight_person_cutoff + (additional_per_person * people_above_8)

        below_federal_poverty_level = (cutoff_value > income)

        return (homelessness or fostercare or eligible_tanf_or_ssi or below_federal_poverty_level)
