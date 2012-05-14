import random as ra

classes      = ['Barbarian', 'Monk', 'Wizard', 'Demon Hunter', 'Witch Doctor']
item_types   = ['off-hand', 'torso', 'head', 'waist', 'hands', 'wrists', 'legs', \
                'feet', 'shoulders', 'ring', 'amulet']
weapon_types = ['1H', '2H']

# Damage Types
dmg_types = ['Physical', 'Lightning', 'Fire', 'Poison', 'Cold', 'Arcane', 'Holy']
PHYSICAL    = dmg_types[0]
LIGHTNING   = dmg_types[1]
FIRE        = dmg_types[2]
POISON      = dmg_types[3]
COLD        = dmg_types[4]
ARCANE      = dmg_types[5]
HOLY        = dmg_types[6]

# Time related vars
DOT_tick_freq = float(1.00) # 1.00 == DOT dmg is assigned every 1 second

class SkillEffect:
    def __init__(self, name, cost, generate=0.00, prctWeaponDmg=0.00, dmgType=dmg_types[0], \
                 prctDOTDmg=0.00, DOTTime=0.00, APSInc=0.00, maxStack=0, incCritRate=0,
                 cooldown=0):
        self.name           = name
        self.cost           = float(cost)
        self.generate       = float(generate)
        self.pctdmg         = float(prctWeaponDmg)
        self.dotdmg         = float(prctDOTDmg)
        self.dottime        = float(DOTTime)
        self.aps_inc        = float(APSInc)
        self.curr_stack     = 0
        self.max_stack      = maxStack
        self.inc_crit_rate  = float(incCritRate)
        self.cooldown       = float(cooldown)
        self.next_time_avail= 0.00

# Generic Skills
Skill_Normal_Swing  = SkillEffect('Weapon Swing', 0, 0, 100, PHYSICAL)

# Barbarian Skills
Skill_Bash          = SkillEffect('Bash', 0, 6, 150, PHYSICAL)
Skill_HotA          = SkillEffect('Hammer of the Ancients', 20, 0, 200, PHYSICAL, incCritRate=5)
Skill_Cleave        = SkillEffect('Cleave', 0, 5, 120, PHYSICAL)
Skill_Frenzy        = SkillEffect('Frenzy', 0, 3, 110, PHYSICAL, APSInc=15, maxStack=5)

# Monk Skills
Skill_FoT           = SkillEffect('Fists of Thunder', 0, 6, 110, LIGHTNING)
Skill_LTK           = SkillEffect('Lashing Tail Kick', 30, 0, 200, PHYSICAL)
Skill_DR            = SkillEffect('Deadly Reach', 0, 6, 110, PHYSICAL)
Skill_CW            = SkillEffect('Crippling Wave', 0, 6, 110, PHYSICAL)
Skill_EP            = SkillEffect('Exploding Palm', 40, 0, 0, prctDOTDmg=220, DOTTime=3)
Skill_WotHF         = SkillEffect('Way of the Hundred Fists', 0, 6, 140, PHYSICAL)

# Demon Hunter
Skill_HA            = SkillEffect('Hungering Arrow', 0, 3, 115, PHYSICAL)
Skill_Impale        = SkillEffect('Impale', 25, 0, 250, PHYSICAL)

# Wizard Skills
Skill_MagicMissile  = SkillEffect('Magic Missile', 0, 0, 110, ARCANE)

# Witch Doctor Skills
Skill_PoisonDart    = SkillEffect('Poison Dart', 10, 0, 100, POISON, prctDOTDmg=40, DOTTime=2)

class Item:
    def __init__(self, type, name, plusMinDmg=0, plusMaxDmg=0, plusArmor=0, \
                 plusAPS=0, plusStr=0, plusDex=0, plusInt=0, plusVit=0, \
                 plusCritRate=0, plusCritDmg=0, plusMoreDmg=0, plusReflectDmg=0, \
                 plusBonusArmor=0, plusDmgRedRng=0, plusDmgRedMelee=0):
        self.type           = type
        self.name           = name
        self.armor          = float(plusArmor)
        self.low_dmg        = float(plusMinDmg)
        self.high_dmg       = float(plusMaxDmg)
        self.aps_inc        = float(plusAPS)
        self.str            = float(plusStr)
        self.dex            = float(plusDex)
        self.int            = float(plusInt)
        self.vit            = float(plusVit)
        self.crit_rate_inc  = float(plusCritRate)
        self.crit_dmg_inc   = float(plusCritDmg)

        self.bonus_dmg      = float(plusMoreDmg)
        self.reflect_dmg    = float(plusReflectDmg)
        self.bonus_armor    = float(plusBonusArmor)
        self.dmg_red_rng    = float(plusDmgRedRng)
        self.dmg_red_melee  = float(plusDmgRedMelee)

    def __repr__(self):
        s = 'Item Type: %s\n\t  ' % self.type
        s+= '     Name: %s\n\t  ' % self.name
        return s

class Weapon(Item):
    def __init__(self, type, name, lowDmg=0, highDmg=0, aps=1.0, plusArmor=0, \
                 plusAPS=0, plusStr=0, plusDex=0, plusInt=0, plusVit=0, \
                 plusCritRate=0, plusCritDmg=0):
        Item.__init__(self, type, name, lowDmg, highDmg, plusArmor, plusAPS, \
                      plusStr, plusDex, plusInt, plusVit, plusCritRate, plusCritDmg)
        self.aps = float(aps)

    def calcAvgDmg(self):
        return (self.low_dmg + self.high_dmg)/2

    def calcDPS(self):
        return self.calcAvgDmg()*self.aps

    def __repr__(self):
        s = '\tWeapon Type: %s\n' % self.type
        s+= '\t       Name: %s\n' % self.name
        s+= '\tLow  Damage: %d\n' % self.low_dmg
        s+= '\tHigh Damage: %d\n' % self.high_dmg
        s+= '\tAttacks/sec: %.2f' % self.aps
        return s
        
class Character:
    def __init__(self, level, className):
        self.level          = float(level)
        self.class_name     = className.upper()
        
        self.rsrc_name_1    = ''
        self.rsrc_name_2    = ''
        self.rsrc_1         = float(0.00)
        self.rsrc_2         = float(0.00)
        
        if className.upper() in ['BARBARIAN', 'BARB']:
            self.base_str   = level * 3.0
            self.main_attr  = self.base_str
        else:
            self.base_str   = level

        if className.upper() in ['MONK', 'DEMON HUNTER', 'DH']:
            self.base_dex   = level * 3.0
            self.main_attr  = self.base_dex
        else:
            self.base_dex   = level
            
        if className.upper() in ['WIZARD', 'WIZ', 'WITCH DOCTOR', 'WD']:
            self.base_int   = level * 3.0
            self.main_attr  = self.base_int
        else:
            self.base_int   = level
            
        self.base_vit       = (level * 2.0) + 10.0
        
        self.crit_rate      = float(5.00)
        self.crit_dmg       = float(50.00)
        
        self.skill_dmg      = float(0.00)
        
        self.base_aps_inc   = float(0.00)
        self.skill_aps_inc  = float(0.00)

        # set item locations to None
        self.head           = None
        self.torso          = None
        self.waist          = None
        self.legs           = None
        self.hands          = None
        self.wrists         = None
        self.feet           = None
        self.shoulders      = None

        self.ring1          = None
        self.ring2          = None
        self.neck           = None
        
        self.mainhand       = None
        self.offhand        = None

        self.items   = [self.head, self.torso, self.waist, self.legs, self.hands, \
                        self.wrists, self.feet, self.shoulders, self.ring1, \
                        self.ring2, self.neck]
        self.weapons = [self.mainhand]
        if isinstance(self.offhand, Weapon): self.items.append(self.offhand)
        else: self.weapons.append(self.offhand)

        # account for innate dmg reduction of melee classes
        if className.upper() in ['MONK', 'BARBARIAN', 'BARB']:
            self.dmg_red    = float(30.00)
        else:
            self.dmg_red    = float(0.00)

        # accumulated values from all relevant items
        self.calcCharStats()

        # initialize skill priority dictionary
        self.skill_priority = {}

    def calcCharStats(self):
        self.str                = self.base_str
        self.dex                = self.base_dex
        self.int                = self.base_int
        self.vit                = self.base_vit
        self.armor              = float(0.00)
        self.bonus_dmg_low      = float(0.00)
        self.bonus_dmg_high     = float(0.00)
        self.crit_rate_inc      = float(0.00)
        self.crit_dmg_inc       = float(0.00)
        self.aps_inc            = self.base_aps_inc

        self.physical_resist    = float(0.00)
        self.lightning_resist   = float(0.00)
        self.fire_resist        = float(0.00)
        self.poison_resist      = float(0.00)
        self.cold_resist        = float(0.00)
        self.arcane_resist      = float(0.00)
        
        for item in self.items:
            if item:
                self.str            += item.str
                self.dex            += item.dex
                self.int            += item.int
                self.vit            += item.vit
                self.armor          += item.armor
                self.bonus_dmg_low  += item.low_dmg
                self.bonus_dmg_high += item.high_dmg
                self.crit_rate_inc  += item.crit_rate_inc
                self.crit_dmg_inc   += item.crit_dmg_inc
                self.aps_inc        += item.aps_inc
                
        for item in self.weapons:
            if item:
                self.str            += item.str
                self.dex            += item.dex
                self.int            += item.int
                self.vit            += item.vit
                self.armor          += item.armor
                self.crit_rate_inc  += item.crit_rate_inc
                self.crit_dmg_inc   += item.crit_dmg_inc

        # make sure to update the main attribute
        self.setMainAttr()

        # adjust armor based on strength (1 str == 1 armor)
        self.armor += self.str

        # adjust resistances (1 int == 0.1 resistance to all)
        self.physical_resist    += (self.int / 10.00)
        self.lightning_resist   += (self.int / 10.00)
        self.fire_resist        += (self.int / 10.00)
        self.poison_resist      += (self.int / 10.00)
        self.cold_resist        += (self.int / 10.00)
        self.arcane_resist      += (self.int / 10.00)

    def setMainAttr(self):
        if self.class_name.upper() in ['BARBARIAN', 'BARB']:
            self.main_attr  = self.str
        elif self.class_name.upper() in ['MONK', 'DEMON HUNTER', 'DH']:
            self.main_attr  = self.dex
        else:
            self.main_attr  = self.int  

    def addItem(self, item):
        if isinstance(item, Weapon):
            self.addWeapon(item)
            return

        if item.type.lower() == 'head':     self.head = item
        elif item.type.lower() == 'torso':  self.torso = item
        elif item.type.lower() == 'waist':  self.waist = item
        elif item.type.lower() == 'legs':   self.legs = item
        elif item.type.lower() == 'hands':  self.hands = item
        elif item.type.lower() == 'wrists': self.wrists = item
        elif item.type.lower() == 'feet':   self.feet = item
        elif item.type.lower() == 'shoulders': self.shoulders = item
        elif item.type.lower() == 'amulet': self.neck = item
        elif item.type.lower() == 'ring':
            if not self.ring1: self.ring1 = item
            elif not self.ring2: self.ring2 = item
            else: raise Exception('RING SWAPPING TO BE IMPLEMENTED','')
        elif item.type.lower() == 'offhand': self.offhand = item
        else: raise Exception('Unknown Item Type', '')
        
        self.items   = [self.head, self.torso, self.waist, self.legs, self.hands, \
                        self.wrists, self.feet, self.shoulders, self.ring1, \
                        self.ring2, self.neck]
        self.weapons = [self.mainhand]
        if isinstance(self.offhand, Weapon): self.weapons.append(self.offhand)
        else: self.items.append(self.offhand)
            
        self.calcCharStats()

    def addWeapon(self, weapon):
        if not isinstance(weapon, Weapon):
            raise Exception('Not an Item', str(type(weapon)))
        if not weapon.type.upper() in weapon_types:
            raise Exception('Item is not a Weapon', '')
        if not self.mainhand:
            self.mainhand = weapon
            self.calcCharStats()
        elif not self.offhand and not weapon.type.upper() == '2H' and \
             not self.mainhand.type.upper() == '2H':
            self.offhand = weapon
            self.calcCharStats()
        else:
            raise Exception('Character already has 2 weapons', '')

        self.items   = [self.head, self.torso, self.waist, self.legs, self.hands, \
                        self.wrists, self.feet, self.shoulders, self.ring1, \
                        self.ring2, self.neck]
        self.weapons = [self.mainhand]
        if isinstance(self.offhand, Weapon): self.weapons.append(self.offhand)
        else: self.items.append(self.offhand)

    def removeWeapon(self, index):
        if index == 1: self.mainhand = None
        elif index == 2: self.offhand = None
        else: raise Exception('Invalid Index', '')

    def isDualWielding(self):
        return isinstance(self.mainhand, Weapon) and isinstance(self.offhand, Weapon)

    def avgBonusItemDmg(self):
        return (self.bonus_dmg_low + self.bonus_dmg_high)/2.00

    def staticDmgAdjustments(self):
        return (1+self.main_attr/100.00)*(1+self.skill_dmg/100.00)

    def staticDmgAdjustmentsForDPS(self):
        if self.isDualWielding():
            return (1.15+self.aps_inc/100.00)*(1.00+(self.crit_rate*self.crit_dmg/10000.00))*(1+self.main_attr/100.00)*(1.00+self.skill_dmg/100.00)
        return (1.00+self.aps_inc/100.00)*(1.00+(self.crit_rate*self.crit_dmg/10000.00))*(1+self.main_attr/100.00)*(1.00+self.skill_dmg/100.00)

    def calcDPS(self):
        if self.isDualWielding():
            effectiveWeaponDPS = (self.mainhand.calcAvgDmg() + self.offhand.calcAvgDmg() + 2*self.avgBonusItemDmg())*self.mainhand.aps*self.offhand.aps/(self.mainhand.aps+self.offhand.aps)
        else:
            effectiveWeaponDPS = (self.mainhand.calcAvgDmg() + self.avgBonusItemDmg())*self.mainhand.aps
        return effectiveWeaponDPS * self.staticDmgAdjustmentsForDPS()

    def calcMinNonCrit(self, weapon):
        low_dmg = 2.00
        if weapon: low_dmg = weapon.low_dmg + self.bonus_dmg_low
        return low_dmg*(1.00+self.main_attr/100.00)*(1.00+self.skill_dmg/100.00)

    def calcMaxNonCrit(self, weapon):
        high_dmg = 3.00
        if weapon: high_dmg = weapon.high_dmg + self.bonus_dmg_high
        return high_dmg*(1.00+self.main_attr/100.00)*(1.00+self.skill_dmg/100.00)

    def calcMinCrit(self, weapon):
        low_dmg = 2.00
        if weapon: low_dmg = weapon.low_dmg + self.bonus_dmg_low
        return low_dmg*(1.00+self.main_attr/100.00)*(1.00+self.skill_dmg/100.00)*(1.00+self.crit_dmg/100.00)

    def calcMaxCrit(self, weapon):
        high_dmg = 3.00
        if weapon: high_dmg = weapon.high_dmg + self.bonus_dmg_high
        return high_dmg*(1.00+self.main_attr/100.00)*(1.00+self.skill_dmg/100.00)*(1.00+self.crit_dmg/100.00)

    def useSkill(self, time):
        for i in self.skill_priority.keys():
            # if skill costs more of resource than we have, skip to next in priority list
            if self.rsrc_1 < self.skill_priority[i].cost:
                continue

            # if skill is not on cooldown
            if (self.skill_priority[i].next_time_avail >= time) or (self.skill_priority[i].next_time_avail == 0.00):
                # Set the cooldown for this skill
                if self.skill_priority[i].cooldown:
                    self.skill_priority[i].next_time_avail = time + self.skill_priority[i].cooldown

                # Update character resource (if skill is a generator increase, else reduce)
                self.rsrc_1 += self.skill_priority[i].generate
                self.rsrc_1 -= self.skill_priority[i].cost

                # Increment stack
                if self.skill_priority[i].max_stack:
                    if self.skill_priority[i].curr_stack < self.skill_priority[i].max_stack:
                        self.skill_priority[i].curr_stack += 1

                # Update Expiration Time
                

                # Adjust Parameters (e.g. Character Attack Speed)
                self.skill_aps_inc = (self.skill_priority[i].aps_inc * self.skill_priority[i].curr_stack)
                
                return self.skill_priority[i]
        return Skill_Normal_Swing

    def printCharStats(self):
        s = 'Character:\n\t'
        s+= 'Type          : %s\n\t' % self.class_name
        s+= 'Level         : %d\n\t' % self.level

        s+= 'Items:\n\t  '
        
        for i in self.items:
            if i: s += str(i) + '\n\t  '
        s=s[:-2]
        
        s+= 'Health        : %d\n\t' % (self.vit * 10)
        s+= 'Strength      : %d\n\t' % self.str
        s+= 'Dexterity     : %d\n\t' % self.dex
        s+= 'Intelligence  : %d\n\t' % self.int
        
        s+= 'Avg Bonus Dmg : %.1f\n\t' % self.avgBonusItemDmg()
        s+= 'APS Incr      : %.2f%%\n\t' % self.aps_inc 
        s+= 'Crit Rate     : %.2f%%\n\t' % (self.crit_rate + self.crit_rate_inc)
        s+= 'Crit Dmg      : %.2f%%\n\t' % (self.crit_dmg + self.crit_dmg_inc)
        s+= 'Armor         : %d\n\t' % self.armor

        s+= 'Dmg Reduction : %.2f%%\n\t' % self.dmg_red
        
        s+= 'Resistances:\n\t  '
        s+= 'Physical    : %.2f%%\n\t  ' % self.physical_resist
        s+= 'Lightning   : %.2f%%\n\t  ' % self.physical_resist
        s+= 'Fire        : %.2f%%\n\t  ' % self.physical_resist
        s+= 'Poison      : %.2f%%\n\t  ' % self.physical_resist
        s+= 'Cold        : %.2f%%\n\t  ' % self.physical_resist
        s+= 'Arcane      : %.2f%%\n\t  ' % self.physical_resist
        return s

    def printWeaponDmg(self):
        s = 'Character Weapon Damage Information:\n'
        if not self.isDualWielding():
            s += '\tDPS           : %.2f\n' % self.calcDPS()
            s += '\tNon-Crit Range: %.2f - %.2f\n' % (self.calcMinNonCrit(char.mainhand), self.calcMaxNonCrit(char.mainhand))
            s += '\tCrit Range    : %.2f - %.2f\n' % (self.calcMinCrit(char.mainhand), self.calcMaxCrit(char.mainhand))
        else:
            s += '\tDPS                     : %.2f\n' % char.calcDPS()
            s += '\tMain Hand Non-Crit Range: %.2f - %.2f\n' % (char.calcMinNonCrit(char.mainhand), char.calcMaxNonCrit(char.mainhand))
            s += '\tMain Hand Crit Range    : %.2f - %.2f\n' % (char.calcMinCrit(char.mainhand), char.calcMaxCrit(char.mainhand))
            s += '\tOff Hand Non-Crit Range : %.2f - %.2f\n' % (char.calcMinNonCrit(char.offhand), char.calcMaxNonCrit(char.offhand))
            s += '\tOff Hand Crit Range     : %.2f - %.2f\n' % (char.calcMinCrit(char.offhand), char.calcMaxCrit(char.offhand))
        return s

    def printWeaponInfo(self):
        s = ''
        if self.mainhand:
            s += 'MainHand Weapon: \n%s\n' % self.mainhand
        if isinstance(self.offhand, Weapon):
            s += 'OffHand  Weapon: \n%s\n' % self.offhand
        return s

class Barbarian(Character):
    def __init__(self, level):
        Character.__init__(self, level, 'Barbarian')
        self.rsrc_name_1 = 'Fury'
        self.skill_priority = {1: Skill_HotA, 2: Skill_Frenzy, 3: Skill_Bash}

class Monk(Character):
    def __init__(self, level):
        Character.__init__(self, level, 'Monk')
        self.rsrc_name_1 = 'Spirit'
        self.skill_priority = {1: Skill_EP, 2: Skill_WotHF}

class DemonHunter(Character):
    def __init__(self, level):
        Character.__init__(self, level, 'Demon Hunter')
        self.rsrc_name_1 = 'Hatred'
        self.rsrc_name_2 = 'Discipline'
        self.skill_priority = {1: Skill_Impale, 2: Skill_HA}

class Wizard(Character):
    def __init__(self, level):
        Character.__init__(self, level, 'Wizard')
        self.rsrc_name_1 = 'Mana'
        self.rsrc_1 = 150.00 + (10.00 * level)
        self.skill_priority = {1: Skill_MagicMissile}

class WitchDoctor(Character):
    def __init__(self, level):
        Character.__init__(self, level, 'Witch Doctor')
        self.rsrc_name_1 = 'Arcane Power'
        self.rsrc_1 = 150.00 + (10.00 * level)
        self.skill_priority = {1: Skill_PoisonDart}

# Enemy - simulates the enemy we are fighting
class Enemy():
    def __init__(self, name='Dummy', level=60, health=100):
        self.name   = name
        self.level  = level
        self.hp     = health
        self.dots   = {}

    def addDOT(self, curr_time, dot_name, dmg_per_tick, num_ticks):
        self.dots[dot_name] = (curr_time, dmg_per_tick, num_ticks)

    def checkDOTs(self, time):
        dotArray = {}
        for dot in self.dots.keys():
            dot_time, dmg_tick, num_ticks = self.dots[dot]
            
            if time >= dot_time: 
                if num_ticks > 1:
                    num_ticks -= 1
                    self.dots[dot] = (time + DOT_tick_freq, dmg_tick, num_ticks)
                    dotArray[dot] = dmg_tick
                else:
                    dotArray[dot] = dmg_tick
                    ended = self.dots.pop(dot)
        return dotArray

# Simulation Environment Class
class SimulEnvironment:
    def __init__(self, character):
        self.time           = float(0.0)
        self.time_next_swing= float(0.0)
        self.char           = character
        self.dual_wield     = self.char.isDualWielding()
        self.active_weapon  = self.char.mainhand
        
        self.total_swings   = 0
        self.dot_dmg        = 0
        self.total_dmg      = 0
        self.num_crits      = 0

    def advanceTimeToNextSwing(self):
        if self.dual_wield: speed_mod = (1.15+(self.char.aps_inc + self.char.skill_aps_inc)/100.00)
        else: speed_mod = (1+(self.char.aps_inc + self.char.skill_aps_inc)/100.00)
        self.time_next_swing = self.time + 1/(self.active_weapon.aps*speed_mod)

    def setWeaponSwing(self):
        if self.dual_wield:
            if self.active_weapon == self.char.mainhand:
                self.active_weapon = self.char.offhand
            else:
                self.active_weapon = self.char.mainhand

    def calculateWeaponDmg(self, skill, useAvgWeaponDmg=False):
        crit = False
        crit_str = ''
        rand_val = ra.randrange(0, 1000.00)
        if rand_val < ((self.char.crit_rate + skill.inc_crit_rate) * 10.00):
            crit = True
            crit_str = '*CRIT* '
        
        if useAvgWeaponDmg:
            rand_dmg = self.active_weapon.calcAvgDmg()*self.char.staticDmgAdjustments()*(1+(self.char.crit_rate*self.char.crit_dmg/10000.00))
        else:
            rand_dmg = ra.uniform(self.char.calcMinNonCrit(self.active_weapon), self.char.calcMaxNonCrit(self.active_weapon))
            if crit:
                self.num_crits += 1
                rand_dmg = ra.uniform(self.char.calcMinCrit(self.active_weapon), self.char.calcMaxCrit(self.active_weapon))
        return (rand_dmg * (skill.pctdmg/100.00)), crit_str

    def doAttack(self, printEachHit, printEachTimestamp, useAvgWeaponDmg):
        s = ''
        if printEachTimestamp: s+= '[%8.2f] :: Next Swing @ %8.2f\n' % (self.time, self.time_next_swing)
        if self.time >= self.time_next_swing:
            self.total_swings += 1
            skill = char.useSkill(self.time)
            curr_dmg, crit_str = self.calculateWeaponDmg(skill, useAvgWeaponDmg)
            self.total_dmg += curr_dmg
            if printEachHit: s += '[%8.2f] :: Uses %s for %d %sDmg [%d %s]' % (self.time, skill.name, curr_dmg, crit_str, self.char.rsrc_1, self.char.rsrc_name_1)
            self.setWeaponSwing()
            self.advanceTimeToNextSwing()
        if s != '': print s

        if self.time >= self.next_report:
            self.next_report = self.time + 30.00
            #print '\n RESULT SUMMERY @ %.2f' % self.time
            #self.printSimulResults()

    def attackEnemy(self, enemy, printEachHit, printEachTimestamp):
        s = ''
        if printEachTimestamp: s+= '[%8.2f] :: Next Swing @ %8.2f\n' % (self.time, self.time_next_swing)

        if self.time >= self.time_next_swing:
            self.total_swings += 1
            skill = char.useSkill(self.time)            
            curr_dmg, crit_str = self.calculateWeaponDmg(skill, False)
            self.total_dmg += curr_dmg
            enemy.hp -= curr_dmg

            if skill.dotdmg:
                curr_dmg, crit_str = self.calculateWeaponDmg(Skill_Normal_Swing, False)
                dot_dmg = curr_dmg * ((skill.dotdmg / 100.00) / skill.dottime) * DOT_tick_freq
                curr_dmg = 0
                enemy.addDOT(self.time, skill.name, dot_dmg, skill.dottime)
            
            if printEachHit: s += '[%8.2f] :: Uses %s for %d %sDmg [%d %s]\n' % (self.time, skill.name, curr_dmg, crit_str, self.char.rsrc_1, self.char.rsrc_name_1)
            self.setWeaponSwing()
            self.advanceTimeToNextSwing()

        dotArray = enemy.checkDOTs(self.time)
        if dotArray:
            for dot in dotArray.keys():
                #dot_dmg, crit_str = self.calculateWeaponDmg(Skill_Normal_Swing, False)
                #dot_dmg = dot_dmg * dotArray[dot]/100.00
                dot_dmg = dotArray[dot]
                if printEachHit: s += '[%8.2f] :: %s DOT ticks for %d Dmg\n' % (self.time, dot, dot_dmg)
                enemy.hp -= dot_dmg
                self.dot_dmg += dot_dmg   
        if s != '': print s[:-1]

    # How much damage can I do over a certain amount of time
    def simulateFightOverTime(self, time, time_inc=0.01, printEachHit=False, printEachTimestamp=False, useAvgWeaponDmg=False):
        self.time           = 0.00
        self.time_next_swing= 0.00
        self.total_swings   = 0.00
        self.total_dmg      = 0.00
        self.dot_dmg        = 0.00
        self.num_crits      = 0.00
        while self.time < time:
            self.doAttack(printEachHit, printEachTimestamp, useAvgWeaponDmg)
            self.time += time_inc

    # How long will it take to do a certain amount of damage
    def simulateFightToReachDmg(self, dmg,  time_inc=0.01, printEachHit=False, printEachTimestamp=False, useAvgWeaponDmg=False):
        self.time           = 0.00
        self.time_next_swing= 0.00
        self.total_swings   = 0.00
        self.total_dmg      = 0.00
        self.dot_dmg        = 0.00
        self.num_crits      = 0.00
        while self.total_dmg < dmg:
            self.doAttack(printEachHit, printEachTimestamp, useAvgWeaponDmg)
            self.time += time_inc

    def simulateFightEnemy(self, enemy, time_inc=0.01, printEachHit=False, printEachTimestamp=False):
        self.time           = 0.00
        self.time_next_swing= 0.00
        self.total_swings   = 0.00
        self.total_dmg      = 0.00
        self.dot_dmg        = 0.00
        self.num_crits      = 0.00
        while enemy.hp > float(0.00):
            self.attackEnemy(enemy, printEachHit, printEachTimestamp)
            self.time += time_inc

    def printSimulResults(self):
        print 'TOTAL DAMAGE DONE  : %d' % (self.total_dmg + self.dot_dmg)
        print '   Attack Damage Done : %d' % (self.total_dmg)
        print '   DOT Damage Done    : %d' % (self.dot_dmg)
        print 'Time Passed        : %.2f seconds == %4.2f minutes' % (self.time, self.time/60.00)
        print 'Effective APS      : %.2f' % (float(self.total_swings)/float(self.time))
        print 'Effective DPS      : %.2f' % (float(self.total_dmg)/float(self.time))
        print 'Effective Crit Rate: %.2f%%' % (float(self.num_crits)*100.00/float(self.total_swings))

if __name__ == '__main__':
    char = Monk(60)

    # Lets equip our character
    # parameters are:
    #             type, name, lowDmg=0, highDmg=0, plusArmor=0, plusAPS=0,\
    #             plusStr=0, plusDex=0, plusInt=0, plusVit=0, \
    #             plusCritRate=0, plusCritDmg=0):
    ring1 = Item('ring', 'Keen Ring of Wounding', 2, 4, plusAPS=5.00)
    char.addItem(ring1)
    char.addItem(ring1)

    rare_helm = Item('head', 'Banished Helmet', plusStr=50, plusVit=10, plusCritRate=2.5)
    char.addItem(rare_helm)

    # Lets arm our character
    # Weapon values are (in order)
    # Weapon Type (either 2H or 1H), Name, Low Dmg, High Dmg, Attacks Per Second
    w1 = Weapon('2H', 'Warmonger', 444, 659, 1.31)
    char.addWeapon(w1)

    # print info about our character
    print char.printCharStats()
    print char.printWeaponInfo()
    print char.printWeaponDmg()

    env = SimulEnvironment(char)
    enemy = Enemy(name='Temp', level=60, health=4000000)
    env.simulateFightEnemy(enemy, 0.01, False)
    print '\n FINAL SUMMARY'
    env.printSimulResults()

    '''
    char.removeWeapon(1)
    print '\n\nNow we compare Dual Wield\n'
    dw1 = Weapon('1H', 'Name1', 17, 30, 1.2)
    dw2 = Weapon('1H', 'Name2', 17, 30, 1.2)
    char.addWeapon(dw1)
    char.addWeapon(dw2)
    print char.printWeaponInfo()
    print char.printWeaponDmg()

    env = SimulEnvironment(char)
    enemy = Enemy(name='Temp', level=60, health=400000)
    env.simulateFightEnemy(enemy, 0.01, True)
    print '\n FINAL SUMMARY'
    env.printSimulResults()
    '''    