import json
import sys

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("config.json not found please refer to the github repo.", file=sys.stderr)
    exit(84)

print('Current configuration:')
print('SMALL_TRADE:', config['SMALL_TRADE'])
print('BIG_TRADE:', config['SYMBOL'])
print('TICK_SIZE:', config['TICK_SIZE'])
print('PAY_THROUGH_TICKS:', config['PAY_THROUGH_TICKS'])
print('SOUND_FILE:', config['SOUND_FILE'])
print('EXCHANGE:', config['EXCHANGE'])

choices = {
    1: 'SMALL_TRADE',
    2: 'BIG_TRADE',
    3: 'SYMBOL',
    4: 'TICK_SIZE',
    5: 'PAY_THROUGH_TICKS',
    6: 'SOUND_FILE',
    7: 'EXCHANGE'
}
while True:
    print('\nWhich parameter would you like to change?')
    print("1: SMALL_TRADE\n2: BIG_TRADE\n3: SYMBOL\n4: TICK_SIZE\n5: PAY_THROUGH_TICKS\n6: SOUND_FILE\n"
          "7: EXCHANGE\n8: EXIT THE CONFIG SETUP")
    choice = int(input('Enter your choice: '))
    if choice == 8:
        break
    key = choices.get(choice)
    if key:
        new_value = input('Enter the new {}: '.format(key))
    else:
        print('\nInvalid choice')
# Write the updated configuration to config.json
with open('config.json', 'w') as f:
    json.dump(config, f)
