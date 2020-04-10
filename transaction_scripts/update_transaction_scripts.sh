rm ./transaction_scripts/*.mv
cp ../testnet_libra/language/stdlib/staged/transaction_scripts/*.mv ./transaction_scripts/
python3 transaction_scripts/gen_scripts.py > bytecodes.txt
