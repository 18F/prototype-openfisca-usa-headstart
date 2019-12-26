# -*- coding: utf-8 -*-

# This file defines variables for the rules.
# See https://openfisca.org/doc/key-concepts/variables.html.

from openfisca_core.model_api import *
from openfisca_country_template.entities import *


class homelessness(Variable):
    value_type = bool
    entity = Family
    definition_period = YEAR
    label = "Homelessness"
    reference = "https://eclkc.ohs.acf.hhs.gov/policy/45-cfr-chap-xiii/1305-2-terms"


class fostercare(Variable):
    value_type = bool
    entity = Family
    definition_period = YEAR
    label = "fostercare"
    reference = "https://eclkc.ohs.acf.hhs.gov/policy/45-cfr-chap-xiii/1305-2-terms"


class eligible_tanf_or_ssi(Variable):
    value_type = bool
    entity = Family
    definition_period = YEAR
    label = "eligible_tanf_or_ssi"
    reference = "https://eclkc.ohs.acf.hhs.gov/policy/45-cfr-chap-xiii/1305-2-terms"


class income(Variable):
    value_type = float
    entity = Family
    label = u"Salary earned by a family for a given year"
    definition_period = YEAR


class household_size(Variable):
    value_type = int
    entity = Family
    label = u"Household size of a family in a given year"
    definition_period = YEAR


class state_or_territory(Variable):
    value_type = str
    entity = Family
    label = u"U.S. state, territory, or district where the family lives"
    definition_period = YEAR
