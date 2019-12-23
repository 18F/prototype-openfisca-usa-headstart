# -*- coding: utf-8 -*-

# This file defines variables for the rules.
# See https://openfisca.org/doc/key-concepts/variables.html.

from openfisca_core.model_api import *
from openfisca_country_template.entities import *


class eligible(Variable):
    value_type = bool
    entity = Family
    definition_period = MONTH
    label = "Eligible for Head Start"

    def formula(family, period):
        homelessness = family('homelessness', period)
        fostercare = family('fostercare', period)
        eligible_tanf_or_ssi = family('eligible_tanf_or_ssi', period)

        return (homelessness or fostercare or eligible_tanf_or_ssi)
