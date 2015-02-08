//left top (10,60)
//right bottom (590,640)

var stage;
var step = 20;
var level = 5;
var score = 0;
var score2 = null;
var worm = [];
var appleBoolean = false;
var apples = [];
var direction = "r";
var scoreText;
var apple;
var view = "mainMenu";
var msg;

function init() {
	stage = new createjs.Stage("game");
	mainMenu();
};

function loadData() {
	msg = {"messageType": "LOAD_REQUEST",};
	window.parent.postMessage(msg, "*");
}

function mainMenu() {
	view = "mainMenu";

	if (worm.length == 0) {
		loadData();
	}

	stage.removeAllChildren();

	var title = new createjs.Text("Worm Game", "40px Arial", "#ff0000");
	title.x = 180;

	var start = new createjs.Text("1: New game", "30px Arial", "#000000");
	start.x = 10;
	start.y = 200;

	var continueGameText = new createjs.Text("2: Continue Game", "30px Arial", "#000000");
	continueGameText.x = 10;
	continueGameText.y = 250;

	var instructions = new createjs.Text("3: Instructions", "30px Arial", "#000000");
	instructions.x = 10;
	instructions.y = 300;

	var settings = new createjs.Text("4: Settings", "30px Arial", "#000000");
	settings.x = 10;
	settings.y = 350;

	stage.addChild(title, start, continueGameText, instructions, settings);
	stage.update();
};

function game() {
	score = 0;
	worm = [];
	appleBoolean = false;
	apples = [];
	direction = "r";

	stage.removeAllChildren();
	var boxGraphics = new createjs.Graphics();
	boxGraphics.setStrokeStyle(1).beginStroke("black").drawRect(-5, 0, 610, 50);

	var box = new createjs.Shape(boxGraphics);

	updateScore();

	var levelText = new createjs.Text("Level: " + level, "30px Arial");
	levelText.x = 300;
	levelText.y = 10;

	var headGraphics = new createjs.Graphics();
	headGraphics.setStrokeStyle(1).beginStroke("black").beginFill("red").drawCircle(0, 0, 10);
	var head = new createjs.Shape(headGraphics);
	head.x = 290;
	head.y = 340;
	worm.push(head);

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

	stage.addChild(box, scoreText, levelText);
	for (var j = 0; j < worm.length; j++) {
		stage.addChild(worm[j]);
	}
	stage.update();
	view = "game";
	createjs.Ticker.setFPS(level*3);
	createjs.Ticker.addEventListener("tick", tick);
	createjs.Ticker.setPaused(false);

};

function continueGame() {
	if (worm.length > 0) {
		stage.removeAllChildren();
		var boxGraphics = new createjs.Graphics();
		boxGraphics.setStrokeStyle(1).beginStroke("black").drawRect(-5, 0, 610, 50);

		var box = new createjs.Shape(boxGraphics);

		updateScore();

		var levelText = new createjs.Text("Level: " + level, "30px Arial");
		levelText.x = 300;
		levelText.y = 10;

		stage.addChild(box, scoreText, levelText, apple);
		for (var j = 0; j < worm.length; j++) {
			stage.addChild(worm[j]);
		}
		stage.update();
		view = "game";
		createjs.Ticker.setFPS(level*3);
		createjs.Ticker.addEventListener("tick", tick);
		createjs.Ticker.setPaused(false);
	}
	else {
		game();
	}
}

function tick(event) {
	if (!createjs.Ticker.getPaused()){
		if (appleBoolean == false) {
			createApple();
		}
		for (var i = worm.length - 1 ; i > 0; i--) {
			worm[i].x = worm[i - 1].x;
			worm[i].y = worm[i - 1].y;
		}
		if (direction == "r") {//right
			worm[0].x += step;
		}
		else if (direction == "u") {//up
			worm[0].y -= step;
		}
		else if (direction == "l") {//left
			worm[0].x -= step;
		}
		else {//down
			worm[0].y += step;
		}
		collision();
		stage.update();
	}
};

function collision() {
	if (worm[0].x < 10 || worm[0].x > 590 || worm[0].y < 60 || worm[0].y > 640) {
		createjs.Ticker.setPaused(true);
		createjs.Ticker.removeEventListener("tick", endGame());
		return;
	}
	for (var i = 1; i < worm.length; i++) {
		if (worm[0].x == worm[i].x && worm[0].y == worm[i].y) {
			createjs.Ticker.setPaused(true);
			createjs.Ticker.removeEventListener("tick", endGame());
			return;
		}
	}
	if (worm[0].x == apples[0].x && worm[0].y == apples[0].y) {
		score += level;
		updateScore();

		stage.removeChild(apple);
		apples = [];
		appleBoolean = false;

		var tailGraphics = new createjs.Graphics();
		tailGraphics.setStrokeStyle(1).beginStroke("black").beginFill("black").drawCircle(0, 0, 10);
		var tail = new createjs.Shape(tailGraphics);
		tail.x =  worm[worm.length - 1].x;
		tail.y = worm[worm.length - 1].y;
		worm.push(tail);
		stage.addChild(tail);
	}
};

function updateScore() {
	stage.removeChild(scoreText);
	scoreText = new createjs.Text("Score: " + score, "30px Arial");
	scoreText.x = 10;
	scoreText.y = 10;
	stage.addChild(scoreText);
};

function createApple() {
	var appleGraphics = new createjs.Graphics();
	appleGraphics.setStrokeStyle(1).beginStroke("black").beginFill("blue").drawCircle(0, 0, 10);
	apple = new createjs.Shape(appleGraphics);
	apple.x = Math.round(Math.random() * 29) * 20 + 10;
	apple.y = Math.round(Math.random() * 29) * 20 + 60;
	apples.push(apple);
	stage.addChild(apple);
	appleBoolean = true;
	for (var i = 0; i < worm.length; i++) {
		if (apple.x == worm[i].x && apple.y == worm[i].y) {
			apples = [];
			stage.removeChild(apple);
			appleBoolean = false;
			createApple();
		}
	}
}

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

	score2 = score;

	score = 0;
	worm = [];
	appleBoolean = false;
	apples = [];
	direction = "r";
	
};

function pauseGame() {
	view = "pauseGame";
	createjs.Ticker.setPaused(true);
	stage.removeAllChildren();

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
};

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

};

function onKeyDown(x) { //listens for wasd-keypress
	if (x.keyCode == 87 && direction != "d" && view == "game") direction = "u";
  	else if (x.keyCode == 65 && direction != "r" && view == "game") direction = "l";
  	else if (x.keyCode == 83 && direction != "u" && view == "game") direction = "d";
  	else if (x.keyCode == 68 && direction != "l" && view == "game") direction = "r";
  	else if (x.keyCode == 49 && view == "game") pauseGame(); // ToDo pause game

  	else if (x.keyCode == 49 && (view == "instructions" || view == "settings")) mainMenu();

  	else if (x.keyCode == 87 && view == "settings" && level < 10) {
  		level += 1;
  		settingsPage()
  	}

  	else if (x.keyCode == 83 && view == "settings" && level > 1) {
  		level -= 1;
  		settingsPage()
  	}

  	else if (x.keyCode == 49 && view == "mainMenu") game();
  	else if (x.keyCode == 50 && view == "mainMenu") continueGame();
  	else if (x.keyCode == 51 && view == "mainMenu") instructionsPage();
  	else if (x.keyCode == 52 && view == "mainMenu") settingsPage();

  	//Submit score
  	else if (x.keyCode == 49 && view == "endGame") {
  		if (score2 != null){
  			msg = {"messageType": "SCORE", "score": score2};
  			window.parent.postMessage(msg, "*");
  			score2 = null;
  		}
  	}
  	else if (x.keyCode == 50 && view == "endGame") mainMenu();

  	else if (x.keyCode == 49 && view == "pauseGame") continueGame();
  	//Save game
  	else if (x.keyCode == 50 && view == "pauseGame") {
  		var playerItems = [];
  		playerItems.push(level);
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
  	}
  	else if (x.keyCode == 51 && view == "pauseGame") {
  		score = 0;
		worm = [];
		appleBoolean = false;
		apples = [];
		direction = "r";
  		mainMenu();
  	}
};
$(document).keydown(onKeyDown);

//Load data from the service
window.addEventListener("message", function(evt) {
	if (evt.data.messageType === "LOAD" && !isNaN(evt.data.gameState.playerItems[0])) {
		score = 0;
		worm = [];
		appleBoolean = false;
		apples = [];
		direction = "r";

		score = parseInt(evt.data.gameState.score);
		level = parseInt(evt.data.gameState.playerItems[0]);
		var wormLength = parseInt(evt.data.gameState.playerItems[1]);

		var headGraphics = new createjs.Graphics();
		headGraphics.setStrokeStyle(1).beginStroke("black").beginFill("red").drawCircle(0, 0, 10);
		var head = new createjs.Shape(headGraphics);
		head.x = parseInt(evt.data.gameState.playerItems[2]);
		head.y = parseInt(evt.data.gameState.playerItems[3]);
		worm.push(head);

		var tailGraphics = new createjs.Graphics();
		tailGraphics.setStrokeStyle(1).beginStroke("black").beginFill("black").drawCircle(0, 0, 10);
		for (var i = 4; i < wormLength + 2; i++) {
			var tail = new createjs.Shape(tailGraphics);
			tail.x =  parseInt(evt.data.gameState.playerItems[i]);
			tail.y = parseInt(evt.data.gameState.playerItems[i + 1]);
			worm.push(tail);
			i++;
		}

		appleBoolean = evt.data.gameState.playerItems[wormLength + 2];
		direction = evt.data.gameState.playerItems[wormLength + 3];

		var appleGraphics = new createjs.Graphics();
		appleGraphics.setStrokeStyle(1).beginStroke("black").beginFill("blue").drawCircle(0, 0, 10);
		apple = new createjs.Shape(appleGraphics);
		apple.x = parseInt(evt.data.gameState.playerItems[wormLength + 4]);
		apple.y = parseInt(evt.data.gameState.playerItems[wormLength + 5]);
		apples.push(apple);
	}
})

init();