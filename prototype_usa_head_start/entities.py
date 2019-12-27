# -*- coding: utf-8 -*-

# This file defines the entities needed by our legislation.
from openfisca_core.entities import build_entity

Family = build_entity(
    key = "family",
    plural = "families",
    label = u'Family means all persons living in the same household who are supported by the child’s parent(s)’ or guardian(s)’ income; and are related to the child’s parent(s) or guardian(s) by blood, marriage, or adoption; or are the child’s authorized caregiver or legally responsible party.',
    doc = '''
    Family means all persons living in the same household who are supported by the child’s parent(s)’ or guardian(s)’ income; and are related to the child’s parent(s) or guardian(s) by blood, marriage, or adoption; or are the child’s authorized caregiver or legally responsible party.

    Reference: https://eclkc.ohs.acf.hhs.gov/policy/45-cfr-chap-xiii/1305-2-terms.
    ''',
    roles = [],
    is_person = True
    )

Person = build_entity(
    key = "person",
    plural = "persons",
    label = u'An individual. The minimal legal entity on which a legislation might be applied.',
    doc = '''
    ''',
    is_person = True,
    roles = [],
    )

entities = [Family, Person]
