import cx_Freeze

executables = [cx_Freeze.Executable('main.py', base = "Win32GUI")]

cx_Freeze.setup(
    name = "My Example Exe App",
    options = {"build_exe" : 
        {"packages" : ["pygame"], "include_files" : ['D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/csv',
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/img', 
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/other',
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/sound',
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/animparticles.py',
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/basechar.py',
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/cutscenes.py',
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/data.py',
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/hnpc.py',
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/level.py',
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/leveltwo.py',
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/notes.py',
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/object.py',
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/player.py',
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/skill.py',
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/texteng.py',
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/ui.py',
                                                     'D:/Desktop/Output/UnnamedAdventureGame/UnnamedAdventureGame/weapon.py']}},
    executables = executables
)