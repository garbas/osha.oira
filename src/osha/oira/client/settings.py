from euphorie.client.settings import AccountSettings
from euphorie.client.settings import DeleteAccount
from euphorie.client.settings import NewEmail
from euphorie.client.country import IClientCountry
from five import grok
from .interfaces import IOSHAClientSkinLayer

grok.templatedir("templates")


class OSHAAccountSettings(AccountSettings):
    grok.context(IClientCountry)
    grok.layer(IOSHAClientSkinLayer)
    grok.name("account-settings")
    grok.template("account-settings")


class OSHADeleteAccount(DeleteAccount):
    grok.context(IClientCountry)
    grok.layer(IOSHAClientSkinLayer)
    grok.name("account-delete")
    grok.template("account-delete")


class OSHANewEmail(NewEmail):
    grok.context(IClientCountry)
    grok.layer(IOSHAClientSkinLayer)
    grok.name("new-email")
    grok.template("new-email")

    ignoreContext = True
