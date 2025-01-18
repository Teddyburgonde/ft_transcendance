const game = document.getElementById("game");
const player1 = document.getElementById("player1");
const player2 = document.getElementById("player2");
const ball = document.getElementById("ball");
const player1ScoreEl = document.getElementById("player1Score");
const player2ScoreEl = document.getElementById("player2Score");

let player1Y = 200;
let player2Y = 200;
let ballX = 390;
let ballY = 240;
let ballSpeedX = 4;
let ballSpeedY = 4;
let player1Score = 0;
let player2Score = 0;
const paddleSpeed = 20;
const ballSpeed = 4;

// Handle Player 1 movement
document.addEventListener("keydown", (e) => {
  if (e.key === "w" && player1Y > 0) player1Y -= paddleSpeed; // Move up
  if (e.key === "s" && player1Y < 400) player1Y += paddleSpeed; // Move down
  player1.style.top = `${player1Y}px`;
});

// AI for Player 2
function moveAI() {
  if (ballY < player2Y + 50 && player2Y > 0) player2Y -= ballSpeed; // Follow ball up
  if (ballY > player2Y + 50 && player2Y < 400) player2Y += ballSpeed; // Follow ball down
  player2.style.top = `${player2Y}px`;
}

// Ball movement
function moveBall() {
  ballX += ballSpeedX;
  ballY += ballSpeedY;

  // Collision with top and bottom walls
  if (ballY <= 0 || ballY >= 480) ballSpeedY *= -1;

  // Collision with paddles
  if (
    (ballX <= 30 && ballY >= player1Y && ballY <= player1Y + 100) || // Player 1 paddle
    (ballX >= 750 && ballY >= player2Y && ballY <= player2Y + 100)  // Player 2 paddle
  ) {
    ballSpeedX *= -1;
  }

  // Scoring
  if (ballX <= 0) {
    player2Score++;
    resetBall();
  }

  if (ballX >= 780) {
    player1Score++;
    resetBall();
  }

  ball.style.left = `${ballX}px`;
  ball.style.top = `${ballY}px`;
  updateScore();
}

// Reset ball position
function resetBall() {
  ballX = 390;
  ballY = 240;
  ballSpeedX *= -1; // Change ball direction
}

// Update score display
function updateScore() {
  player1ScoreEl.textContent = player1Score;
  player2ScoreEl.textContent = player2Score;
}

// Game loop
function gameLoop() {
  moveAI();
  moveBall();
  requestAnimationFrame(gameLoop);
}

gameLoop();
