from pysnmp.hlapi import *
from .scanner import Scanner
from typing import Dict, Any, TYPE_CHECKING
from ..target import Target

if TYPE_CHECKING:
    from ..core import Config


class SNMP(Scanner):
    def __init__(
        self,
        cred: Dict[str, Any],
        target: Target,
        username: str,
        password: str,
        config: "Config",
    ) -> None:
        super(SNMP, self).__init__(cred, target, config, username, password)

    def fingerprint(self) -> bool:
        # Don't fingerprint since it's UDP
        return True

    def _check(self) -> str:
        iterator = getCmd(
            SnmpEngine(),
            CommunityData(self.password),
            UdpTransportTarget((str(self.target.host), 161)),
            ContextData(),
            ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
        )

        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        evidence = ""
        if errorIndication:
            self.logger.debug(errorIndication)
        elif errorStatus:
            self.logger.debug(
                f"{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}"
            )
        else:
            for varBind in varBinds:
                evidence += " = ".join([x.prettyPrint() for x in varBind])

        if evidence == "":
            raise Exception

        return evidence

    def _mkscanner(self, cred: Dict[str, Any], target: Target, u: str, p: str, config: "Config") -> "SNMP":
        return SNMP(cred, target, u, p, config)
