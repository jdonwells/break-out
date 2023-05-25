@namespace
class SpriteKind:
    Ball = SpriteKind.create()
    Border = SpriteKind.create()
    Brick = SpriteKind.create()

def on_on_overlap(sprite, otherSprite):
    disableBall()
    music.play(music.melody_playable(music.buzzer),
        music.PlaybackMode.IN_BACKGROUND)
    info.change_life_by(-1)
    newBall()
sprites.on_overlap(SpriteKind.Ball, SpriteKind.Border, on_on_overlap)

def on_on_overlap2(sprite2, otherSprite2):
    global VXNew
    sprite2.bottom = otherSprite2.top
    VXNew = (ball.x - playerSprite.x) * ballBounceAngleMultiplier + ball.vx
    ball.set_velocity(VXNew, 0 - ball.vy)
    music.play(music.melody_playable(music.thump),
        music.PlaybackMode.IN_BACKGROUND)
sprites.on_overlap(SpriteKind.Ball, SpriteKind.player, on_on_overlap2)

def dropTheBall():
    global ball
    ball = sprites.create(assets.image("""
        Ball
    """), SpriteKind.Ball)
    ball.set_position(startX(), scene.screen_height() / 2)
    ball.set_velocity(0, 70)
    ball.set_bounce_on_wall(True)
def createBackground():
    global outOfBounds
    scene.set_background_color(15)
    outOfBounds = sprites.create(assets.image("""
        outOfBounds
    """), SpriteKind.Border)
    outOfBounds.set_position(scene.screen_width() / 2, scene.screen_height() - 2)
def createBricks():
    global brickHeight, BrickWidth, bricksYOffset, brickXOffset, brickColors, PointsPerLevel, XbyRow, pointsByRow, brick
    brickHeight = 8
    BrickWidth = 16
    bricksYOffset = 20
    brickXOffset = BrickWidth / 2
    brickColors = [assets.image("""
            redBrick
        """),
        assets.image("""
            greenBrick
        """),
        assets.image("""
            blueBrick
        """),
        assets.image("""
            purpleBrick
        """),
        assets.image("""
            yellowBrick
        """)]
    PointsPerLevel = 0
    for row in range(5):
        XbyRow = row * brickHeight + bricksYOffset
        pointsByRow = 1 + 2 * (4 - row)
        column = 0
        while column <= int(scene.screen_width() / BrickWidth) - 1:
            brick = sprites.create(brickColors[row], SpriteKind.Brick)
            brick.set_position(column * BrickWidth + brickXOffset, XbyRow)
            sprites.set_data_number(brick, "points", pointsByRow)
            PointsPerLevel += pointsByRow
            column += 1
def NewLevel():
    disableBall()
    createBricks()
    newBall()
def startX():
    return scene.screen_width() / 2 - BrickWidth / 2

def on_life_zero():
    game.game_over(False)
info.on_life_zero(on_life_zero)

def createPlayer():
    global playerSprite
    playerSprite = sprites.create(assets.image("""
        paddle
    """), SpriteKind.player)
    controller.move_sprite(playerSprite, 120, 0)
    playerSprite.set_position(startX(), scene.screen_height() - 10)
    playerSprite.set_stay_in_screen(True)
def disableBall():
    ball.set_position(startX(), scene.screen_height() / 2)
    ball.set_velocity(0, 0)

def on_on_overlap3(sprite3, otherSprite3):
    global canBounce
    info.change_score_by(sprites.read_data_number(otherSprite3, "points"))
    music.play(music.melody_playable(music.ba_ding),
        music.PlaybackMode.IN_BACKGROUND)
    sprites.destroy(otherSprite3, effects.disintegrate, 100)
    if info.score() % PointsPerLevel == 0:
        info.change_life_by(1)
        NewLevel()
    else:
        if canBounce:
            canBounce = False
            ball.vy = 0 - ball.vy
            pause(200)
            canBounce = True
sprites.on_overlap(SpriteKind.Ball, SpriteKind.Brick, on_on_overlap3)

def newBall():
    sprites.destroy(playerSprite)
    createPlayer()
    pause(2000)
    sprites.destroy(ball)
    dropTheBall()
brick: Sprite = None
pointsByRow = 0
XbyRow = 0
PointsPerLevel = 0
brickColors: List[Image] = []
brickXOffset = 0
bricksYOffset = 0
BrickWidth = 0
brickHeight = 0
outOfBounds: Sprite = None
playerSprite: Sprite = None
ball: Sprite = None
VXNew = 0
canBounce = False
ballBounceAngleMultiplier = 0
game.splash("BREAK OUT!", "Press A to begin")
ballBounceAngleMultiplier = 3
info.set_score(0)
info.set_life(3)
canBounce = True
createBackground()
createBricks()
createPlayer()
dropTheBall()