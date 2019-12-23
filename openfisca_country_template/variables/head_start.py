# -*- coding: utf-8 -*-

# This file defines variables for the rules.
# See https://openfisca.org/doc/key-concepts/variables.html.

from openfisca_core.model_api import *
from openfisca_country_template.entities import *


class homelessness(Variable):
    value_type = bool
    entity = Family
    definition_period = MONTH
    label = "Homelessness"
    reference = "https://eclkc.ohs.acf.hhs.gov/policy/45-cfr-chap-xiii/1305-2-terms"


class eligible(Variable):
    value_type = bool
    entity = Family
    definition_period = MONTH
    label = "Eligible for Head Start"

    def formula(family, period):
        homelessness = family('homelessness', period)
        return homelessness