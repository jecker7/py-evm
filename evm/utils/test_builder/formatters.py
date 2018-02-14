from cytoolz import (
    compose,
)
from eth_utils import (
    combine_argument_formatters,
    encode_hex,
    int_to_big_endian,
    to_checksum_address,
)
import cytoolz.curried
import eth_utils.curried


int_to_hex = compose(encode_hex, int_to_big_endian)

environment_formatter = eth_utils.curried.apply_formatters_to_dict({
    "currentCoinbase": to_checksum_address,
    "currentDifficulty": int_to_hex,
    "currentGasLimit": int_to_hex,
    "currentNumber": int_to_hex,
    "currentTimestamp": int_to_hex,
    "previousHash": encode_hex,
})


storage_item_formatter = combine_argument_formatters(int_to_hex, int_to_hex)
storage_formatter = cytoolz.curried.itemmap(storage_item_formatter)


account_state_formatter = eth_utils.curried.apply_formatters_to_dict({
    "balance": int_to_hex,
    "nonce": int_to_hex,
    "code": encode_hex,
    "storage": storage_formatter,
})


state_item_formatter = combine_argument_formatters(to_checksum_address, account_state_formatter)
state_formatter = cytoolz.curried.itemmap(state_item_formatter)


transaction_group_formatter = eth_utils.curried.apply_formatters_to_dict({
    "data": eth_utils.curried.apply_formatter_to_array(encode_hex),
    "gasLimit": eth_utils.curried.apply_formatter_to_array(int_to_hex),
    "gasPrice": int_to_hex,
    "nonce": int_to_hex,
    "secretKey": encode_hex,
    "to": to_checksum_address,
    "value": eth_utils.curried.apply_formatter_to_array(int_to_hex),
})


expect_element_formatter = eth_utils.curried.apply_formatters_to_dict({
    "result": state_formatter
})
expect_formatter = eth_utils.curried.apply_formatter_to_array(expect_element_formatter)


test_formatter = eth_utils.curried.apply_formatters_to_dict({
    "env": environment_formatter,
    "pre": state_formatter,
    "transaction": transaction_group_formatter,
    "expect": expect_formatter,
})


filler_formatter = cytoolz.curried.valmap(test_formatter)


post_formatter = eth_utils.curried.apply_formatters_to_dict({
    "hash": encode_hex
})


filled_formatter = cytoolz.curried.valmap(eth_utils.curried.apply_formatters_to_dict({
    "env": environment_formatter,
    "pre": state_formatter,
    "transaction": transaction_group_formatter,
    "post": post_formatter,
}))