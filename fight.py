from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from create_bot import bot

from random import randint

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_attack = InlineKeyboardMarkup().\
        add(InlineKeyboardButton(text='Атака', callback_data='attack'))

#тетстовый словарь персонажа
player_characters_dict = {"hungry": 100,
                          "thirst": 100,
                          "tired": 10000,
                          "inventory_size": 0,
                          "inventory_size_max": 25,

                          "power": 10,
                          "instinct": 10,
                          "agility": 10,
                          "stamina": 10,
                          "intelligence": 10,
                          "lucky": 10,
                          "mutation": 0,

                          "critical_damage_chance": 10,
                          "dodge_chance": 20,
                          "armor": 5,
                          "damage": [2,4],
                          "mutation_resist": 0,
                          "cold_resist": 0,
                          "heat_resist": 0}

# Тестовый враг
enemy_characters_dict = {
                            "name": 'Крыса',
                            "power": 10,
                            "instinct": 10,
                            "agility": 10,
                            "stamina": 1,
                            "intelligence": 10,
                            "lucky": 10,
                            "mutation": 0,

                            "critical_damage_chance": 5,
                            "dodge_chance": 15,
                            "armor": 0,
                            "damage": [1,3],
                            "mutation_resist": 0,
                            "cold_resist": 0,
                            "heat_resist": 0}

# Здороье
async def helth(character: dict):
    helth = character["stamina"]*10
    return helth

# Расчёт урона
async def damage(character: dict, enemy: dict):
    
    damage_list = character["damage"]
    dodge_chance = enemy["dodge_chance"]
    critical_damage_chance = character["critical_damage_chance"]
    is_crit = False
    is_dodge = False


    if randint(1, 101) > dodge_chance:
        if randint(1, 101) <= critical_damage_chance:
            damage = randint(damage_list[0], damage_list[1]) *2
            is_crit = True
        else:
            damage = randint(damage_list[0], damage_list[1])
    else:
        damage = 0
        is_dodge = True

    

    return damage, is_crit, is_dodge

async def place_to_attack_block():
    pta = randint(1,3) # Место для атаки
    ptb = randint(1,3) # Место блока
    return pta, ptb

#текст для атаки
async def text_attack(name_enemy, enemy_damage, player_damege):
    pta_player, ptb_player = await place_to_attack_block() # место для атаки игрока
    pta_enemy, ptb_enemy = await place_to_attack_block() # место для атаки противника

    player_text = ''
    enemy_text = ''

    is_block_pl = False
    is_block_en = False

    if pta_player == ptb_enemy: 
        is_block_pl = True # игрок попал в бок
        if pta_player == 1:
            player_text = f'🎖🛡Ты атакуешь {name_enemy} в голову, но попадаешь в блок🛡'   
        elif pta_player == 2:
            player_text = f'🎖🛡Ты атакуешь {name_enemy} в корпус, но попадаешь в блок🛡'
        elif pta_player == 3:
            player_text = f'🎖🛡Ты атакуешь {name_enemy} в ноги, но попадаешь в блок🛡'
    else:
        is_block_pl = False
        if pta_player == 1:
            player_text = f'🎖Ты атакуешь {name_enemy} в голову и наносишь🗡: {player_damege} урона🎉'   
        elif pta_player == 2:
            player_text = f'🎖Ты атакуешь {name_enemy} в корпус и наносишь🗡: {player_damege} урона🎉'
        elif pta_player == 3:
            player_text = f'🎖Ты атакуешь {name_enemy} в ноги и наносишь🗡: {player_damege} урона🎉'

    if pta_enemy == ptb_player:
        is_block_en = True # враг попал в бок
        if pta_enemy == 1:
            enemy_text = f'🎖🛡{name_enemy} атакует тебя в голову, но попадает в блок🛡'   
        elif pta_enemy == 2:
            enemy_text = f'🎖🛡{name_enemy} атакует тебя в корпус, но попадает в блок🛡'
        elif pta_enemy == 3:
            enemy_text = f'🎖🛡{name_enemy} атакует тебя в ноги, но попадает в блок🛡'
    else:
        is_block_en = False
        if pta_enemy == 1:
            enemy_text = f'🎖{name_enemy} атакует тебя в голову и наносит🗡: {enemy_damage} урона🤕'   
        elif pta_enemy == 2:
            enemy_text = f'🎖{name_enemy} атакует тебя в корпус и наносит🗡: {enemy_damage} урона🤕'
        elif pta_enemy == 3:
            enemy_text = f'🎖{name_enemy} атакует тебя в ноги и наносит🗡: {enemy_damage} урона🤕'

    return player_text, enemy_text, is_block_pl, is_block_en

#Старт боя
async def start_fight(message: types.Message, state:FSMContext):

    enemy_dict = enemy_characters_dict      #ЗАМЕНИТЬ НА СЛОВАРЬ ИЗ БД
    helth_enemy = await helth(enemy_dict)   # КАК ПОЯВИТСЯ ЗНАЧЕНИЕ ЗДОРОВЬЕ В СЛОВАРЕ ЗАМЕНИТЬ НА НЕГО
    name_enemy = enemy_dict["name"]
    player_dict = player_characters_dict    #ЗАМЕНИТЬ НА СЛОВАРЬ ИЗ БД
    helth_player = await helth(player_dict) # КАК ПОЯВИТСЯ ЗНАЧЕНИЕ ЗДОРОВЬЕ В СЛОВАРЕ ЗАМЕНИТЬ НА НЕГО
    
    # ФОТО ЗАМЕНИТЬ НА ФОТО ИЗ БД
    await message.answer_photo(photo=open('image/rat.png', 'rb'), caption=f'⚔️На вас напала {name_enemy}'+
    ' и скалит зубы.⚔️\n\n'+
    f'Её здоровье❤️: {helth_enemy}\n'+
    f'Твоё здоровье❤️: {helth_player}', reply_markup=button_attack)
    
    await state.set_state('fight')
    await state.update_data(enemy_dict=enemy_dict, name_enemy=name_enemy, helth_enemy=helth_enemy,\
        player_dict=player_dict, helth_player=helth_player)


# Метод атаки из стостояни в бою
async def attack(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    
    name_enemy = data["name_enemy"]

    damage_enemy, is_crit_enemy, is_dodge_player = await damage(data["enemy_dict"], data["player_dict"])
    damage_player, is_crit_player, is_dodge_enemy = await damage(data["enemy_dict"], data["player_dict"])
    
    player_text, enemy_text, is_block_pl, is_block_en = await text_attack(name_enemy, damage_enemy, damage_player)

    if is_block_pl:
        damage_player = 0
    if is_block_en:
        damage_enemy = 0

    current_helth_enemy = data['helth_enemy'] - damage_player
    curent_helth_player = data['helth_player'] - damage_enemy
        
    if is_dodge_enemy and is_dodge_player:
        text= f'⚔️Вы обменялись бы смачными ударами с крысой, если бы кто-то из вас попал.⚔️\n\n'\
            f'Её здоровье❤️: {current_helth_enemy}\n'\
            f'Твоё здоровье❤️: {curent_helth_player}'  
    elif is_dodge_enemy:
        if is_block_en:
            text= f'⚔️{name_enemy} уворачивается от твоей атаки ⚔️\n\n'\
                    f'{enemy_text}\n\n' \
                    f'Её здоровье❤️: {current_helth_enemy}\n'\
                    f'Твоё здоровье❤️: {curent_helth_player}'
        else:
            if is_crit_enemy:
                text= f'⚔️{name_enemy} уварачивается и кусает тебя за самое догорое. Это критическое попадание❗️⚔️ \n\n'\
                    +f'{enemy_text}\n\n' \
                    f'Её здоровье❤️: {current_helth_enemy}\n'\
                    f'Твоё здоровье❤️: {curent_helth_player}'           
            else:
                text= f'⚔️Крыса кусает тебя за палец и не даёт себя ударить! ⚔️\n\n'\
                    f'{enemy_text}\n\n' \
                    f'Её здоровье❤️: {current_helth_enemy}\n'\
                    f'Твоё здоровье❤️: {curent_helth_player}'     
            
    elif is_dodge_player:
        if is_block_pl:
            text= f'⚔️Ты уходишь в уклонение. ⚔️\n\n'\
                    f'{player_text}\n\n' \
                    f'Её здоровье❤️: {current_helth_enemy}\n'\
                    f'Твоё здоровье❤️: {curent_helth_player}'
        else:
            if is_crit_player:
                text= f'⚔️Ты делаешь финт, избегая укуса, и бъёшь крысу крисиным приёмом. Это критическое попадание❗️ ⚔️\n\n'\
                    f'{player_text}\n\n' \
                    f'Её здоровье❤️: {current_helth_enemy}\n'\
                    f'Твоё здоровье❤️: {curent_helth_player}'              
            else:
                text= f'⚔️Ты уходишь в уклонение, и бъёшь крысу ногой по почкам. ⚔️\n\n'\
                    f'{player_text}\n\n' \
                    f'Её здоровье❤️: {current_helth_enemy}\n'\
                    f'Твоё здоровье❤️: {curent_helth_player}'
    else:
            if is_crit_enemy and not is_block_en:
                text= f'⚔️Крыса кусает тебя за самое ценное, но ты успеваешь ей вмазать. ⚔️\n\n'\
                    f'{player_text}\n' \
                    f'{enemy_text} и это крит❗️\n\n'\
                    f'Её здоровье❤️: {current_helth_enemy}\n'\
                    f'Твоё здоровье❤️: {curent_helth_player}'
            elif is_crit_player and not is_block_pl:
                text= f'⚔️Крыса кусает тебя, но ты успеваешь дать ей по зубам. ⚔️\n\n'\
                    f'{player_text} и это крит❗️\n' \
                    f'{enemy_text}\n\n'\
                    f'Её здоровье❤️: {current_helth_enemy}\n'\
                    f'Твоё здоровье❤️: {curent_helth_player}'
            elif is_crit_enemy and is_block_en:
                text= f'⚔️Крыса кусает тебя за самое ценное, но ты успеваешь ей вмазать. ⚔️\n\n'\
                    f'{player_text}\n' \
                    f'{enemy_text}\n\n'\
                    f'Её здоровье❤️: {current_helth_enemy}\n'\
                    f'Твоё здоровье❤️: {curent_helth_player}'
            elif is_crit_player and is_block_pl:
                text= f'⚔️Крыса кусает тебя, но ты успеваешь дать ей по зубам. ⚔️\n\n'\
                    f'{player_text}\n' \
                    f'{enemy_text}\n\n'\
                    f'Её здоровье❤️: {current_helth_enemy}\n'\
                    f'Твоё здоровье❤️: {curent_helth_player}'
            elif (is_crit_enemy and is_crit_player) and not (is_block_pl and is_block_en):
                text= f'⚔️Крыса нажадит когтями твоё слабое место, но ты успеваешь ткнуть её в глаз. ⚔️\n\n'\
                    f'{player_text} и это крит❗️\n' \
                    f'{enemy_text} и это крит❗️\n\n'\
                    f'Её здоровье❤️: {current_helth_enemy}\n'\
                    f'Твоё здоровье❤️: {curent_helth_player}'
            elif (is_crit_enemy and is_crit_player) and is_block_pl:
                text= f'⚔️Крыса нажадит когтями твоё слабое место, но ты успеваешь ткнуть её в глаз. ⚔️\n\n'\
                    f'{player_text}\n' \
                    f'{enemy_text} и это крит❗️\n\n'\
                    f'Её здоровье❤️: {current_helth_enemy}\n'\
                    f'Твоё здоровье❤️: {curent_helth_player}'
            elif (is_crit_enemy and is_crit_player) and is_block_en:
                text= f'⚔️Крыса нажадит когтями твоё слабое место, но ты успеваешь ткнуть её в глаз. ⚔️\n\n'\
                    f'{player_text} и это крит❗️\n' \
                    f'{enemy_text}\n\n'\
                    f'Её здоровье❤️: {current_helth_enemy}\n'\
                    f'Твоё здоровье❤️: {curent_helth_player}'
            else:
                text= f'⚔️Вы обменялись смачными ударами с крысой. ⚔️\n\n'\
                    f'{player_text}\n' \
                    f'{enemy_text}\n\n'\
                    f'Её здоровье❤️: {current_helth_enemy}\n'\
                    f'Твоё здоровье❤️: {curent_helth_player}'
   
    
    if curent_helth_player <=0:
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer('Бой закончен!')
        await call.message.answer_photo(photo=open('image/dead_man.jpg', 'rb'),\
            caption='☠️Кажется крыса сейчас позавёт друзей на пир. Ты мёртв💔☠️') #заменить на фото из бд
        await state.reset_state()
    elif current_helth_enemy <= 0:
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer('Бой закончен!')
        await call.message.answer_photo(photo=open('image/dead_rat.webp', 'rb'),\
            caption='🎉Крыса мертва!💔 Поздравляю, одним невинным животным меньше🎉')#заменить на фото из бд
        await state.reset_state()
    else:
        await call.message.edit_reply_markup(reply_markup=None)    
        await call.message.answer(text=text, reply_markup=button_attack)



    await state.update_data(helth_enemy=current_helth_enemy, helth_player=curent_helth_player)




# Регистрация хендреров ВЫЗВАТЬ ПРИ СТАРТЕ БОТА
def register_hendlers_fight(dp : Dispatcher):
    dp.register_message_handler(start_fight, commands=['fight'])
    dp.register_callback_query_handler(attack, state='fight')