from libra.on_chain_config.libra_version import LibraVersion
from libra.on_chain_config.validator_set import ValidatorSet
from libra.on_chain_config.vm_publishing_option import VMPublishingOption
from libra.event import EventKey
from libra.account_config import AccountConfig


# State sync will panic if the value of any config in this registry is uninitialized
ON_CHAIN_CONFIG_REGISTRY = [
    VMPublishingOption.get_config_id(),
    LibraVersion.get_config_id(),
    ValidatorSet.get_config_id(),
]


def new_epoch_event_key() -> EventKey:
    return EventKey.new_from_address(AccountConfig.association_address(), 4)
