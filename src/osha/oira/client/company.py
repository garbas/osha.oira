from five import grok
from zope import schema
from zope.interface import directlyProvides
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from z3c.form import button
from euphorie.client import model
from osha.oira.client import model as oshamodel
from euphorie.client.company import Company as GenericCompany
from euphorie.client.company import CompanySchema as GenericCompanySchema
from euphorie.client.session import SessionManager
# from plone.directives import form
from .interfaces import IOSHAReportPhaseSkinLayer
from .. import _

grok.templatedir("templates")


class CompanySchema(GenericCompanySchema):

    needs_met = schema.Choice(
        title=_(
            "label_needs_met",
            default=u"Did this OiRA tool meet to your needs?"),
        vocabulary=SimpleVocabulary([
            SimpleTerm(True, title=_("label_yes", default=u"Yes")),
            SimpleTerm(False, title=_("label_no", default=u"No")),
        ]),
        required=False
    )
    recommend_tool = schema.Choice(
        title=_(
            "label_recommend_tool",
            default=u"Would you recommend this OiRA tool to an enterprise "
            u"similar to yours ?"),
        vocabulary=SimpleVocabulary([
            SimpleTerm(True, title=_("label_yes", default=u"Yes")),
            SimpleTerm(False, title=_("label_no", default=u"No")),
        ]),
        required=False
    )


class Company(GenericCompany):
    """ Override the class from euphorie.client to add our own layer.
    """
    grok.layer(IOSHAReportPhaseSkinLayer)
    grok.template("report_company")

    schema = CompanySchema

    def _assertCompany(self):
        if self.company is not None:
            return
        session = SessionManager.session
        if session.company is None:
            session.company = oshamodel.Company()
        directlyProvides(session.company, CompanySchema)
        self.company = session.company

    @button.buttonAndHandler(u"Previous")
    def handlePrevious(self, action):
        url = "%s/report" % self.request.survey.absolute_url()
        self.request.response.redirect(url)

    @button.buttonAndHandler(u"Next")
    def handleNext(self, action):
        (data, errors) = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        url = "%s/report/view" % self.request.survey.absolute_url()
        self.request.response.redirect(url)

    @button.buttonAndHandler(u"Skip")
    def handleSkip(self, action):
        # XXX: This a hack. We need to know if a company report has been
        # skipped but can't add new SQL columns. So we mark the country 'xx'.
        # (Country field is restricted to 3 chars). For #4436.
        data = {
            'conductor': None,
            'country': u'xx',
            'employees': None,
            'referer': None,
            'workers_participated': None,
            'needs_met': None,
            'recommend_tool': None,
        }
        self.applyChanges(data)
        url = "%s/report/view" % self.request.survey.absolute_url()
        self.request.response.redirect(url)
