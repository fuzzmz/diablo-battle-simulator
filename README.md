Diablo 3 battle simulator
=========================

This is a simple python script for generating battles in Diablo 3.

**This is not my script!** I've found it on the [Battle.net forums](us.battle.net/d3/en/forum/topic/4926623342) and decided to give it a proper home.

The script currently:

- Understands an Item as something having a Type ['off-hand', 'torso', 'head', 'waist', 'hands', 'wrists', 'legs', 'feet', 'shoulders', 'ring', 'amulet'], a name and some extra stats (probably not all covered yet).
- Understands a Weapon as an Enhanced Item that adds the concept of "attacks per second"
- Understands the 5 main classes
- Understands the following stats for a class: Str, Dex, Int, Vit, Armor, Resists
- Understands that characters have items (for the most part, swapping out items isn't yet fully in there, especially rings)
- Understands Weapons and the concept of Offhand being potentially a Dual Wield situations, and you can't dual wield when using a 2H weapon
- Has math for calculating dmg of a weapon and skills
- Has basic understanding of Skills that a class can perform with arguments for Cost, Generators (gains of resource), % Weapon Dmg, DOTs, APS Increase, Type of Dmg (Physical, Fire, etc.), etc.
- Has a very very rudimentary skill rotation in place (which will get scrapped and replaced eventually by a much smarter system, perhaps a self evolving genetic one even) which accounts for Skill Cost or Resource Generation
- Most classes are functional (except for DH where it only tracks Hatred right now and not Discipline usage yet)
- There is a built-in simulator that can either track how long it takes to do some amount of damage  OR  how much dmg can be done over some amount of time
- Resists and Mitigation for mobs and their level is not yet built in
- Enemies don't exist and don't fight back which prevents calculating the value of slows, stuns, knockbacks, etc...