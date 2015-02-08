//left top (10,60)
//right bottom (590,640)

var stage;
var step = 20;
var level = 5;
var score = 0;
var worm = [];
var appleBoolean = false;
var apples = [];
var direction = "r";
var scoreText;
var apple;
var menu = true;

function init() {
	stage = new createjs.Stage("game");
	mainMenu();
};

function mainMenu() {
	stage.removeAllChildren();

	var title = new createjs.Text("Worm", "40px Arial", "#000000");
	title.x = 250;

	var start = new createjs.Text("Start game", "30px Arial", "#000000");
	start.x = 10;
	start.y = 200;

	var instructions = new createjs.Text("Instructions", "30px Arial", "#000000");
	instructions.x = 10;
	instructions.y = 300;

	var settings = new createjs.Text("Settings", "30px Arial", "#000000");
	settings.x = 10;
	settings.y = 400;

	stage.addChild(title, start, instructions, settings);
	stage.update();
};

function game() {
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
	menu = false;
	createjs.Ticker.setFPS(level*3);
	createjs.Ticker.addEventListener("tick", tick);
	createjs.Ticker.setPaused(false);

};

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
	menu = true;
	stage.removeAllChildren();
	stage.addChild(scoreText);
	score = 0;
	worm = [];
	appleBoolean = false;
	apples = [];
	direction = "r";
	scoreText.addEventListener("click", mainMenu);
};

function instructionsPage() {
	stage.removeAllChildren();
	stage.update();
};

function settingsPage() {
	stage.removeAllChildren();

	var levelSetting = new createjs.Text("Taso: " + level, "30px Arial", "#000000");
	levelSetting.x = 10;
	levelSetting.y = 200;

	var wallSetting = new createjs.Text("Seinä: " + level, "30px Arial", "#000000");
	wallSetting.x = 10;
	wallSetting.y = 300;

	stage.addChild(levelSetting, wallSetting);
	stage.update();

};

function onKeyDown(x) { //listens for wasd-keypress
	if (x.keyCode == 87 && direction != "d") direction = "u";
  	if (x.keyCode == 65 && direction != "r") direction = "l";
  	if (x.keyCode == 83 && direction != "u") direction = "d";
  	if (x.keyCode == 68 && direction != "l") direction = "r";
  	if (x.keyCode == 49 && menu == true) game();
  	if (x.keyCode == 50 && menu == true) instructionsPage();
  	if (x.keyCode == 51 && menu == true) settingsPage();
};
$(document).keydown(onKeyDown);

init();