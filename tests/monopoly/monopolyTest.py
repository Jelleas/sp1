import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import importlib

import os
import sys

parpath = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir))
sys.path.append(parpath)

from notAllowedCode import *

def before():
	import matplotlib.pyplot as plt
	plt.switch_backend("Agg")
	lib.neutralizeFunction(plt.pause)
	# lib.neutralizeFunction(matplotlib.use)

def after():
	import matplotlib.pyplot as plt
	plt.switch_backend("TkAgg")
	importlib.reload(plt)

@t.test(0)
def hasthrow_two_dice(test):

	notAllowed = {"break": "break"}
	notAllowedCode(test, lib.source(_fileName), notAllowed)

	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "throw_two_dice")
	test.description = lambda : "defines the function throw_two_dice"
	test.timeout = lambda : 60

@t.passed(hasthrow_two_dice)
@t.test(10)
def correctDice(test):
	test.test = lambda : assertlib.between(lib.getFunction("throw_two_dice", _fileName)(), 2, 12)
	test.description = lambda : "returns a correct value for a throw with two dice"
	test.timeout = lambda : 120

@t.passed(correctDice)
@t.test(20)
def hassimulate_monopolyAndsimulate_monopoly_games(test):

	def testMethod():
		test_game = assertlib.fileContainsFunctionDefinitions(_fileName, "simulate_monopoly")
		test_games = assertlib.fileContainsFunctionDefinitions(_fileName, "simulate_monopoly_games")
		info = ""
		if not test_game:
			info = "the function simulate_monopoly has not been defined"
		elif not test_games:
			info = "the function simulate_monopoly has been defined :) \n  -the function simulate_monopoly_games has not yet been defined"
		return test_game and test_games, info



	test.test = lambda : testMethod()
	test.description = lambda : "defines the functions simulate_monopoly and simulate_monopoly_games"
	test.timeout = lambda : 60


@t.passed(hassimulate_monopolyAndsimulate_monopoly_games)
@t.test(30)
def correctAverageTrump(test):

	def testMethod():
		nArguments = len(lib.getFunction("simulate_monopoly_games", _fileName).arguments)

		# Trump
		if nArguments == 1:
			testInput = lib.getFunction("simulate_monopoly_games", _fileName)(1000)
			test.success = lambda info : "The code works without starting_money, you can now proceed with starting_money!"
			if assertlib.sameType(lib.getFunction("simulate_monopoly_games", _fileName)(10000), None):
				test.fail = lambda info : "Make sure that the function simulate_monopoly_games returns the average required number of throws and nothing else"

		# starting money, 1 player
		elif nArguments == 2:
			testInput = lib.getFunction("simulate_monopoly_games", _fileName)(1000, 1000000)
			if assertlib.sameType(lib.getFunction("simulate_monopoly_games", _fileName)(10000, 1000000), None):
				test.fail = lambda info : "Make sure that the function simulate_monopoly_games returns the average required number of throws and nothing else"

		# starting money 2 player
		elif nArguments == 3:
			testInput = lib.getFunction("simulate_monopoly_games", _fileName)(1000, 1000000, 0)
			if assertlib.sameType(lib.getFunction("simulate_monopoly_games", _filename)(1000, 1000000, 0), None):
				test.fail = lambda info : "Make sure that the function simulate_monopoly_games returns the average required number of throws and nothing else"

		else:
			testInput = False
			test.fail = lambda info : "Make sure that the function simulate_monopoly_games with Trumpmode uses 1 argument and with starting_money 2 arguments"

		return testInput

	test.test = lambda : assertlib.between(testMethod(), 145, 149)
	test.test = lambda : testMethod()
	test.description = lambda : "Monopoly works for Trumpmode"
	test.timeout = lambda : 120


@t.passed(correctAverageTrump)
@t.test(40)
def correctAverageStartingMoney(test):

	def testMethod():
		nArguments = len(lib.getFunction("simulate_monopoly_games", _fileName).arguments)

		if nArguments == 2:
			testInput = lib.getFunction("simulate_monopoly_games", _fileName)(10000, 1500)
			if assertlib.sameType(lib.getFunction("simulate_monopoly_games", _fileName)(10000, 1500), None):
				test.fail = lambda info : "Make sure that the function simulate_monopoly_games returns the average required number of throws and nothing else"
			return testInput
		elif nArguments == 3:
			testInput = lib.getFunction("simulate_monopoly_games", _fileName)(10000, 1500, 0)
			if assertlib.sameType(lib.getFunction("simulate_monopoly_games", _fileName)(10000, 1500, 0), None):
				test.fail = lambda info : "Make sure that the function simulate_monopoly_games returns the average required number of throws and nothing else"
			return testInput
		else:
			return 0

	test.test = lambda : assertlib.between(testMethod(), 184, 189)
	test.description = lambda : "Monopoly works with 1500 euro starting_money"
	test.timeout = lambda : 60
