//left top (10,60)
//right bottom (590,640)
/* global createjs, $ */

"use strict";
var stage;
var step = 20;
var scoreText;
var view = "mainMenu";
var msg;

var score = 0;
var level = 5;
var worm = [];
var appleBoolean = false;
var apple;
var apples = [];
var direction = "r";

var saved_data = false;
var saved_score = 0;
var saved_level = 0;
var saved_worm = [];
var saved_appleBoolean = false;
var saved_apple;
var saved_apples = [];
var saved_direction = "r";

// Initialize canvas
function init() {
	stage = new createjs.Stage("game");
	loadData();
	setTimeout(function(){
		mainMenu();
	}, 500);
}

// Ask for saved data from the service
function loadData() {
	msg = {"messageType": "LOAD_REQUEST",};
	window.parent.postMessage(msg, "*");
}

// Main menu
function mainMenu() {
	view = "mainMenu";
	stage.removeAllChildren();
	resetGame();

	var title = new createjs.Text("Worm Game", "40px Arial", "#ff0000");
	title.x = 180;

	if (saved_data === true) {
		var continueGameText = new createjs.Text("1: Continue Game", "30px Arial", "#000000");
		continueGameText.x = 10;
		continueGameText.y = 200;
		stage.addChild(continueGameText);
	}

	var start = new createjs.Text("2: New game", "30px Arial", "#000000");
	start.x = 10;
	start.y = 250;

	var instructions = new createjs.Text("3: Instructions", "30px Arial", "#000000");
	instructions.x = 10;
	instructions.y = 300;

	var settings = new createjs.Text("4: Settings", "30px Arial", "#000000");
	settings.x = 10;
	settings.y = 350;

	stage.addChild(title, start, instructions, settings);
	stage.update();
}

// Resets the game variables
function resetGame(){
	score = 0;
	worm = [];
	appleBoolean = false;
	apples = [];
	direction = "r";
}

// Start a new game
function newGame() {
	initializeGame();

	// Create worms head
	var headGraphics = new createjs.Graphics();
	headGraphics.setStrokeStyle(1).beginStroke("black").beginFill("red").drawCircle(0, 0, 10);
	var head = new createjs.Shape(headGraphics);
	head.x = 290;
	head.y = 340;
	worm.push(head);

	// Create rest of the worm
	var tailGraphics = new createjs.Graphics();
	tailGraphics.setStrokeStyle(1).beginStroke("black").beginFill("black").drawCircle(0, 0, 10);
	var i = 20;
	while (i < 60) {
		var tail = new createjs.Shape(tailGraphics);
		tail.x =  290 - i;
		tail.y = 340;
		worm.push(tail);
		i += 20;
	}

	startGame();
}

// Continue a paused or saved game
function continueGame() {
	// If called from main menu continue a saved game else continue a paused game
	if (view === "mainMenu") {
		transferData();
	}

	initializeGame();

	stage.addChild(apple);

	startGame();
}

// Initializes the game view
function initializeGame() {
	view = "game";
	stage.removeAllChildren();

	var boxGraphics = new createjs.Graphics();
	boxGraphics.setStrokeStyle(1).beginStroke("black").drawRect(-5, 0, 610, 50);
	var box = new createjs.Shape(boxGraphics);

	updateScore();

	var levelText = new createjs.Text("Level: " + level, "30px Arial");
	levelText.x = 300;
	levelText.y = 10;

	stage.addChild(box, scoreText, levelText);
}

// Starts the game
function startGame() {
	for (var j = 0; j < worm.length; j++) {
		stage.addChild(worm[j]);
	}

	stage.update();

	createjs.Ticker.setFPS(level*3);
	createjs.Ticker.addEventListener("tick", tick);
	createjs.Ticker.setPaused(false);
}

// Game animation
function tick() {
	if (!createjs.Ticker.getPaused()){
		// Create a new apple if previuous is eaten
		if (appleBoolean === false) {
			createApple();
		}
		for (var i = worm.length - 1 ; i > 0; i--) {
			worm[i].x = worm[i - 1].x;
			worm[i].y = worm[i - 1].y;
		}
		// Right
		if (direction == "r") {
			worm[0].x += step;
		}
		// Up
		else if (direction == "u") {
			worm[0].y -= step;
		}
		// Left
		else if (direction == "l") {
			worm[0].x -= step;
		}
		// Down
		else {
			worm[0].y += step;
		}
		collision();
		stage.update();
	}
}

// Detects collisions
function collision() {
	// Collision with a wall
	if (worm[0].x < 10 || worm[0].x > 590 || worm[0].y < 60 || worm[0].y > 640) {
		createjs.Ticker.setPaused(true);
		createjs.Ticker.removeEventListener("tick", endGame());
		return;
	}
	// Collision with the worm itself
	for (var i = 1; i < worm.length; i++) {
		if (worm[0].x == worm[i].x && worm[0].y == worm[i].y) {
			createjs.Ticker.setPaused(true);
			createjs.Ticker.removeEventListener("tick", endGame());
			return;
		}
	}
	// Collision with an apple
	if (worm[0].x == apples[0].x && worm[0].y == apples[0].y) {
		score += level;
		updateScore();

		// Remove the eaten apple
		stage.removeChild(apple);
		apples = [];
		appleBoolean = false;

		// Add one ball to the end of the worm
		var tailGraphics = new createjs.Graphics();
		tailGraphics.setStrokeStyle(1).beginStroke("black").beginFill("black").drawCircle(0, 0, 10);
		var tail = new createjs.Shape(tailGraphics);
		tail.x =  worm[worm.length - 1].x;
		tail.y = worm[worm.length - 1].y;
		worm.push(tail);
		stage.addChild(tail);
	}
}

// Updates the score in game view
function updateScore() {
	stage.removeChild(scoreText);
	scoreText = new createjs.Text("Score: " + score, "30px Arial");
	scoreText.x = 10;
	scoreText.y = 10;
	stage.addChild(scoreText);
}

// Creates a new apple when the previous is eaten
function createApple() {
	var appleGraphics = new createjs.Graphics();
	appleGraphics.setStrokeStyle(1).beginStroke("black").beginFill("blue").drawCircle(0, 0, 10);
	apple = new createjs.Shape(appleGraphics);
	apple.x = Math.round(Math.random() * 29) * 20 + 10;
	apple.y = Math.round(Math.random() * 29) * 20 + 60;
	apples.push(apple);
	stage.addChild(apple);
	appleBoolean = true;
	// If apple is created on top of the worm, delete it and call the creation function again
	for (var i = 0; i < worm.length; i++) {
		if (apple.x == worm[i].x && apple.y == worm[i].y) {
			apples = [];
			stage.removeChild(apple);
			appleBoolean = false;
			createApple();
		}
	}
}

// When when the worm dies display end game view
function endGame() {
	view = "endGame";
	stage.removeAllChildren();

	var endTitle = new createjs.Text("Game Over", "40px Arial", "#ff0000");
	endTitle.x = 190;
	endTitle.y = 0;

	var endScore = new createjs.Text("Your score was: " + score, "35px Arial", "#ff0000");
	endScore.x = 10;
	endScore.y = 200;

	var submitScore = new createjs.Text("1: Submit score", "30px Arial", "#000000");
	submitScore.x = 10;
	submitScore.y = 250;

	var endMainMenu= new createjs.Text("2: Return to main menu", "30px Arial", "#000000");
	endMainMenu.x = 10;
	endMainMenu.y = 300;

	stage.addChild(endTitle, endScore, submitScore, endMainMenu);
	stage.update();	
}

// Pause the game
function pauseGame() {
	view = "pauseGame";
	stage.removeAllChildren();

	createjs.Ticker.setPaused(true);
	
	var pauseTitle = new createjs.Text("Paused", "40px Arial", "#000000");
	pauseTitle.x = 220;
	pauseTitle.y = 0;

	var pauseContinue = new createjs.Text("1: Continue", "30px Arial", "#000000");
	pauseContinue.x = 10;
	pauseContinue.y = 200;

	var pauseSave = new createjs.Text("2: Save game", "30px Arial", "#000000");
	pauseSave.x = 10;
	pauseSave.y = 250;

	var pauseExit = new createjs.Text("3: Exit game", "30px Arial", "#000000");
	pauseExit.x = 10;
	pauseExit.y = 300;

	stage.addChild(pauseTitle, pauseContinue, pauseSave, pauseExit);
	stage.update();
}

// Display game instructions
function instructionsPage() {
	view = "instructions";
	stage.removeAllChildren();

	var instructionsTitle = new createjs.Text("Instructions", "40px Arial", "#000000");
	instructionsTitle.x = 200;
	instructionsTitle.y = 0;

	var instructions1 = new createjs.Text("Feed the worm as many apples as possible", "30px Arial", "#000000");
	instructions1.x = 10;
	instructions1.y = 200;

	var instructions2 = new createjs.Text("without running into walls or itself.", "30px Arial", "#000000");
	instructions2.x = 10;
	instructions2.y = 250;

	var instructions3 = new createjs.Text("Use WASD-keys to control the worm.", "30px Arial", "#000000");
	instructions3.x = 10;
	instructions3.y = 300;

	var instructions4 = new createjs.Text("Press 1 to pause the game.", "30px Arial", "#000000");
	instructions4.x = 10;
	instructions4.y = 350;

	var instructionsBack = new createjs.Text("1: Back", "30px Arial", "#000000");
	instructionsBack.x = 10;
	instructionsBack.y = 500;

	stage.addChild(instructionsTitle, instructions1, instructions2, instructions3, instructions4, instructionsBack);
	stage.update();
}

// Display game settings
function settingsPage() {
	view = "settings";
	stage.removeAllChildren();

	var settingsTitle = new createjs.Text("Settings", "40px Arial", "#000000");
	settingsTitle.x = 220;
	settingsTitle.y = 0;

	var levelSetting = new createjs.Text("Level: " + level, "30px Arial", "#ff0000");
	levelSetting.x = 10;
	levelSetting.y = 200;

	var settingInstruction = new createjs.Text("Use W and S keys to change the level.", "30px Arial", "#000000");
	settingInstruction.x = 10;
	settingInstruction.y = 250;

	var settingsBack = new createjs.Text("1: Back", "30px Arial", "#000000");
	settingsBack.x = 10;
	settingsBack.y = 500;

	stage.addChild(settingsTitle, levelSetting, settingInstruction, settingsBack);
	stage.update();
}

// Save current game
function saveGame() {
	// Send data to be saved to the service
	var playerItems = [];
	playerItems.push(level);
	// Save the length of the worm (*2). This information is used when loading the data
	playerItems.push(worm.length*2);
	for (var i = 0; i < worm.length; i++) {
		playerItems.push(worm[i].x);
		playerItems.push(worm[i].y);
	}
	playerItems.push(appleBoolean);
	playerItems.push(direction);
	playerItems.push(apple.x);
	playerItems.push(apple.y);

	msg = {"messageType": "SAVE", "gameState": {"playerItems": playerItems, "score": score}};
	window.parent.postMessage(msg, "*");

	var gameSaved = new createjs.Text("Game has been saved!", "30px Arial", "#ff0000");
	gameSaved.x = 10;
	gameSaved.y = 500;

	stage.addChild(gameSaved);
	stage.update();

	// Save data to the game
	saved_data = true;
	saved_score = score;
	saved_level = level;
	saved_worm = worm;
	saved_appleBoolean = appleBoolean;
	saved_apple = apple;
	saved_apples = apples;
	saved_direction = direction;
}

// Transfer saved data to current data to continue saved game
function transferData() {
	if (saved_data){
		score = saved_score;
		level = saved_level;
		worm = saved_worm;
		appleBoolean = saved_appleBoolean;
		apple = saved_apple;
		apples = saved_apples;
		direction = saved_direction;
	}
}

// Submit highscore to the service
function submitScore() {
	msg = {"messageType": "SCORE", "score": score};
	window.parent.postMessage(msg, "*");

	var scoreSubmitted = new createjs.Text("Score has been submitted!", "30px Arial", "#ff0000");
	scoreSubmitted.x = 10;
	scoreSubmitted.y = 500;

	stage.addChild(scoreSubmitted);
	stage.update();
}

// Listens for key presses
function onKeyDown(x) {
	if (x.keyCode === 87 && direction !== "d" && view === "game") direction = "u"; // Up
  	else if (x.keyCode === 65 && direction !== "r" && view === "game") direction = "l"; // Left
  	else if (x.keyCode === 83 && direction !== "u" && view === "game") direction = "d"; // Down
  	else if (x.keyCode === 68 && direction !== "l" && view === "game") direction = "r"; // Right
  	else if (x.keyCode === 49 && view == "game") pauseGame(); // Pause game

  	 // Back to main menu from instruction and settings page
  	else if (x.keyCode === 49 && (view === "instructions" || view === "settings")) mainMenu();

  	// Increase level
  	else if (x.keyCode === 87 && view === "settings" && level < 10) {
  		level += 1;
  		settingsPage();
  	}
  	// Decrease level
  	else if (x.keyCode === 83 && view === "settings" && level > 1) {
  		level -= 1;
  		settingsPage();
  	}

  	// Continue a saved game
  	else if (x.keyCode === 49 && view === "mainMenu" && saved_data === true) continueGame();
  	// Start a new game
  	else if (x.keyCode === 50 && view === "mainMenu") newGame();
  	// Display instructions page
  	else if (x.keyCode === 51 && view === "mainMenu") instructionsPage();
  	// Display settings page
  	else if (x.keyCode === 52 && view === "mainMenu") settingsPage();

  	// Submit your highscore after game
  	else if (x.keyCode === 49 && view === "endGame") submitScore();
  	// Return to main menu
  	else if (x.keyCode === 50 && view === "endGame") {
		setTimeout(function(){
			mainMenu();
		}, 500);
	}

  	// Continue a paused game
  	else if (x.keyCode === 49 && view === "pauseGame") continueGame();
  	// Save current game
  	else if (x.keyCode === 50 && view === "pauseGame") saveGame();
  	// Exit the game without saving and return to main menu
  	else if (x.keyCode === 51 && view === "pauseGame") {
		setTimeout(function(){
			mainMenu();
		}, 500);
	}
}

$(document).keydown(onKeyDown);

//Load data from the service
window.addEventListener("message", function(evt) {
	if (evt.data.messageType === "LOAD" && !isNaN(evt.data.gameState.playerItems[0])) {
		saved_data = true;
		saved_score = parseInt(evt.data.gameState.score);
		saved_level = parseInt(evt.data.gameState.playerItems[0]);
		var wormLength = parseInt(evt.data.gameState.playerItems[1]);

		// Clear saved worm
		saved_worm = [];

		// Create worms head object from saved data
		var headGraphics = new createjs.Graphics();
		headGraphics.setStrokeStyle(1).beginStroke("black").beginFill("red").drawCircle(0, 0, 10);
		var head = new createjs.Shape(headGraphics);
		head.x = parseInt(evt.data.gameState.playerItems[2]);
		head.y = parseInt(evt.data.gameState.playerItems[3]);
		saved_worm.push(head);

		// Craete rest of the worm from saved data
		var tailGraphics = new createjs.Graphics();
		tailGraphics.setStrokeStyle(1).beginStroke("black").beginFill("black").drawCircle(0, 0, 10);
		for (var i = 4; i < wormLength + 2; i++) {
			var tail = new createjs.Shape(tailGraphics);
			tail.x =  parseInt(evt.data.gameState.playerItems[i]);
			tail.y = parseInt(evt.data.gameState.playerItems[i + 1]);
			saved_worm.push(tail);
			i++;
		}

		saved_appleBoolean = evt.data.gameState.playerItems[wormLength + 2];
		saved_direction = evt.data.gameState.playerItems[wormLength + 3];

		// Clear saved apples
		saved_apples = [];

		// Create apple object from saved data
		var appleGraphics = new createjs.Graphics();
		appleGraphics.setStrokeStyle(1).beginStroke("black").beginFill("blue").drawCircle(0, 0, 10);
		saved_apple = new createjs.Shape(appleGraphics);
		saved_apple.x = parseInt(evt.data.gameState.playerItems[wormLength + 4]);
		saved_apple.y = parseInt(evt.data.gameState.playerItems[wormLength + 5]);
		saved_apples.push(saved_apple);
	}
	else if (evt.data.messageType === "MESSAGE") {
		if (evt.data.message === "NO SAVED DATA") {
			saved_data = false;
		}
	}
});

init();