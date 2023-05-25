namespace SpriteKind {
    export const Ball = SpriteKind.create()
    export const Border = SpriteKind.create()
    export const Brick = SpriteKind.create()
}
sprites.onOverlap(SpriteKind.Ball, SpriteKind.Border, function (sprite, otherSprite) {
    disableBall()
    music.play(music.melodyPlayable(music.buzzer), music.PlaybackMode.InBackground)
    info.changeLifeBy(-1)
    newBall()
})
sprites.onOverlap(SpriteKind.Ball, SpriteKind.Player, function (sprite2, otherSprite2) {
    sprite2.bottom = otherSprite2.top
    VXNew = (ball.x - playerSprite.x) * ballBounceAngleMultiplier + ball.vx
    ball.setVelocity(VXNew, 0 - ball.vy)
    music.play(music.melodyPlayable(music.thump), music.PlaybackMode.InBackground)
})
function dropTheBall () {
    ball = sprites.create(assets.image`Ball`, SpriteKind.Ball)
    ball.setPosition(startX(), scene.screenHeight() / 2)
    ball.setVelocity(0, 70)
    ball.setBounceOnWall(true)
}
function createBackground () {
    scene.setBackgroundColor(15)
    outOfBounds = sprites.create(assets.image`outOfBounds`, SpriteKind.Border)
    outOfBounds.setPosition(scene.screenWidth() / 2, scene.screenHeight() - 2)
}
sprites.onOverlap(SpriteKind.Ball, SpriteKind.Brick, function (sprite3, otherSprite3) {
    info.changeScoreBy(sprites.readDataNumber(otherSprite3, "points"))
    music.play(music.melodyPlayable(music.baDing), music.PlaybackMode.InBackground)
    sprites.destroy(otherSprite3, effects.disintegrate, 100)
    if (info.score() % PointsPerLevel == 0) {
        info.changeLifeBy(1)
        NewLevel()
    } else if (canBounce) {
        canBounce = false
        ball.vy = 0 - ball.vy
        pause(200)
        canBounce = true
    }
})
function createBricks () {
    let column: number;
brickHeight = 8
    BrickWidth = 16
    bricksYOffset = 20
    brickXOffset = BrickWidth / 2
    brickColors = [
    assets.image`redBrick`,
    assets.image`greenBrick`,
    assets.image`blueBrick`,
    assets.image`purpleBrick`,
    assets.image`yellowBrick`
    ]
    PointsPerLevel = 0
    for (let row = 0; row <= 4; row++) {
        XbyRow = row * brickHeight + bricksYOffset
        pointsByRow = 1 + 2 * (4 - row)
        column = 0
        while (column <= Math.trunc(scene.screenWidth() / BrickWidth) - 1) {
            brick = sprites.create(brickColors[row], SpriteKind.Brick)
            brick.setPosition(column * BrickWidth + brickXOffset, XbyRow)
            sprites.setDataNumber(brick, "points", pointsByRow)
            PointsPerLevel += pointsByRow
            column += 1
        }
    }
}
function NewLevel () {
    disableBall()
    createBricks()
    newBall()
}
function startX () {
    return scene.screenWidth() / 2 - BrickWidth / 2
}
info.onLifeZero(function () {
    game.gameOver(false)
})
function createPlayer () {
    playerSprite = sprites.create(assets.image`paddle`, SpriteKind.Player)
    controller.moveSprite(playerSprite, 120, 0)
    playerSprite.setPosition(startX(), scene.screenHeight() - 10)
    playerSprite.setStayInScreen(true)
}
function disableBall () {
    ball.setPosition(startX(), scene.screenHeight() / 2)
    ball.setVelocity(0, 0)
}
function newBall () {
    sprites.destroy(playerSprite)
    createPlayer()
    pause(2000)
    sprites.destroy(ball)
    dropTheBall()
}
let brick: Sprite = null
let pointsByRow = 0
let XbyRow = 0
let brickColors: Image[] = []
let brickXOffset = 0
let bricksYOffset = 0
let BrickWidth = 0
let brickHeight = 0
let PointsPerLevel = 0
let outOfBounds: Sprite = null
let playerSprite: Sprite = null
let ball: Sprite = null
let VXNew = 0
let canBounce = false
let ballBounceAngleMultiplier = 0
game.splash("BREAK OUT!", "Press A to begin")
ballBounceAngleMultiplier = 3
info.setScore(0)
info.setLife(3)
canBounce = true
createBackground()
createBricks()
createPlayer()
dropTheBall()
