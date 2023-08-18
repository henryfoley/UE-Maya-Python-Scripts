#import TestingUI
#import importlib
#importlib.reload(TestingUI)
#TestingUI.myUI()

import maya.cmds as cmds

def myUI():
    if cmds.window('TestingUI', exists=True):
        print('Window exists! Deleting window!')
        cmds.deleteUI('TestingUI', window=True)

    cmds.window('TestingUI', sizeable=True)

    cmds.columnLayout('mainUI_C', parent='TestingUI')

    cmds.rowColumnLayout(nc=1, cw=[(1, 300)], p='mainUI_C')
    cmds.separator(h=10, style='none')

    cmds.rowColumnLayout(nc=3, cw=[(1,100),(2,100),(3,100)],cs=[(1,10),(2,10),(3,10)], p='mainUI_C')
    cmds.button(l='Do Something', command=lambda args:buttonAction('Hello World'))
    cmds.button(l='Do Two', command=lambda args:buttonAction('Hello There'))
    cmds.button(l='FF Update', command=lambda args:floatFieldUpdate())

    cmds.rowColumnLayout(nc=1,cw=[(1,330)], p='mainUI_C')
    cmds.separator(h=10, style='in')

    cmds.rowColumnLayout(nc=1, cw=[(1,200)], cs=[(1,50)], p='mainUI_C')
    cmds.textField('buttonDoesSomething_TF', text='Hello There!')

    cmds.rowColumnLayout(nc=1,cw=[(1,330)], p='mainUI_C')
    cmds.separator(h=10, style='in')

    cmds.rowColumnLayout(nc=2, cw=[(1,100),(2,100)],cs=[(1,90),(2,10)], p='mainUI_C')
    cmds.checkBox(l='Hello', value=True)
    cmds.checkBox(l='World', value=False)
    cmds.floatField('first_FF', minValue=0.00, maxValue=100000.0, step=10, v=0.0)
    cmds.floatField('second_FF', minValue=0.00, maxValue=100000.0, step=10, v=0.0)


    cmds.rowColumnLayout(nc=1, cw=[(1, 300)], p='mainUI_C')
    cmds.separator(h=10, style='in')

    cmds.rowColumnLayout(nc=3, cw=[(1,100),(2,100),(3,100)],cs=[(1,10),(2,10),(3,10)], p='mainUI_C')
    cmds.radioCollection('rc_collection')
    cmds.radioButton('button1', l='Button 1', sl=True)
    cmds.radioButton('button2', l='Button 2')
    cmds.radioButton('button3', l='Button 3')

    cmds.showWindow('TestingUI')

def buttonAction(op):
    print('The Button Works')
    cmds.textField('buttonDoesSomething_TF', edit=True, text=op)

def floatFieldUpdate():
    ffValue = cmds.floatField('first_FF', query=True, value=True)
    cmds.floatField('second_FF', edit=True, value=ffValue)