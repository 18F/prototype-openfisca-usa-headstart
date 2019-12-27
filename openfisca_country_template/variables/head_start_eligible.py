# -*- coding: utf-8 -*-

# This file defines variables for the rules.
# See https://openfisca.org/doc/key-concepts/variables.html.

from openfisca_core.model_api import *
from openfisca_country_template.entities import *


# class HeadStartEligibilityStatus(Enum):
#     eligible = u'Appears eligible for Head Start. Eligibility does not guarantee a spot. If program is over-capacity, consult Head Start guidance on selection.'
#     appears_ineligible = u'Appears ineligible for Head Start.'


class head_start_eligibility_status(Variable):
    value_type = bool
    # possible_values = HeadStartEligibilityStatus
    # default_value = HeadStartEligibilityStatus.appears_ineligible
    entity = Family
    definition_period = YEAR
    label = u"Head Start Eligibility Status"

    def formula(family, period, parameters):
        homelessness = family('homelessness', period)
        fostercare = family('fostercare', period)
        eligible_tanf_or_ssi = family('eligible_tanf_or_ssi', period)

        # TODO: Get Head Start input on this "early return" strategy
        if (homelessness or fostercare or eligible_tanf_or_ssi):
            return True

        income = family('income', period)
        household_size = family('household_size', period)
        state_or_territory = family('state_or_territory', period)

        federal_poverty_level_data = parameters(period).federal_poverty_level
        fpl_guidelines = federal_poverty_level_data

        if ((state_or_territory == 'AK') or (state_or_territory == 'HI')):
            # TODO: Not sure why state_or_territory is being sent in as array here
            local_guidelines = fpl_guidelines[state_or_territory[0]]
        else:
            local_guidelines = fpl_guidelines.forty_eight_states_plus_dc

        if (9 > household_size):
            # TODO: Not sure why household_size is being sent in as array here
            household_size_key = str(household_size[0]) + "_person_household"
            cutoff_value = local_guidelines[household_size_key]
        else:
            eight_person_cutoff = local_guidelines["8_person_household"]
            additional_per_person = local_guidelines["additional_per_person_above_8"]
            people_above_8 = household_size - 8
            cutoff_value = eight_person_cutoff + (additional_per_person * people_above_8)

        below_federal_poverty_level = (cutoff_value > income)

        return below_federal_poverty_level
