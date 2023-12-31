#!/usr/bin/env python

import os
import re
import toml
import subprocess

keyfile = "./script/new-keypair.json"
programs_path = "./programs"
path_object = os.walk(programs_path)
path_list = list(path_object)
print(path_list)
path=path_list[0][1][0]
print(path)

# mkdir -p ./target/deploy
dirshell = ['mkdir', '-p', './target/deploy']
ok = subprocess.run(dirshell, capture_output=True, text=True)

# solana-keygen new -s --force --no-bip39-passphrase -o new-keypair.json
shell = ['solana-keygen', 'new', '-s', '--force', '--no-bip39-passphrase', '-o', keyfile]
result1 = subprocess.run(shell, capture_output=True, text=True)
print(result1.stdout)

# cp -f ./script/new-keypair.json ./target/deploy/solana_nft_anchor-keypair.json
cpshell = ['cp', '-f', keyfile, f'./target/deploy/{path}-keypair.json']
subprocess.run(cpshell, capture_output=True, text=True)
print("create new keypair file: ", f"./target/deploy/{path}-keypair.json")

# solana address -k ./script/new-keypair.json
solanashell = ['solana', 'address', '-k', keyfile]
result2 = subprocess.run(solanashell, capture_output=True, text=True)

addr = result2.stdout.replace("\n", "")
print("ProjectId: ", addr)

declare_id_regex = r"^(([\w]+::)*)declare_id!\(\"(\w*)\"\)"

rsfile = f"./programs/{path}/src/lib.rs"
with open(rsfile, 'r') as file:
    libdata = file.read()

    change_str = f'declare_id!("{addr}")'
    libresult = re.sub(declare_id_regex, change_str, libdata, 0, re.MULTILINE)

with open(rsfile, 'w') as file:
    file.write(libresult)

tomlfile = "./Anchor.toml"
with open(tomlfile, 'r') as file:
   tomldata = toml.load(file)

tomldata['programs']['localnet']['solana_nft_anchor'] = addr

with open(tomlfile, 'w') as file:
    toml.dump(tomldata, file)
