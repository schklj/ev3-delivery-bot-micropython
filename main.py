#!/usr/bin/env pybricks-micropython

#импортируем модули необходимые для работы с железом блока
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, GyroSensor, InfraredSensor, Motor, TouchSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.tools import DataLog, StopWatch, wait

#инициализируем объект, в который входят кнопки, светодиоды, дисплей и динамик блока
block = EV3Brick()

#инициализация моторов поступательного движения
left_wheel = Motor(Port.B, Direction.CLOCKWISE)
right_wheel = Motor(Port.C, Direction.CLOCKWISE)

#инициализация мотора вращательного движения
steering = Motor(Port.A, Direction.CLOCKWISE)

#инициализация внешник сенсоров
line_sensor = ColorSensor(Port.S1)
gyro = GyroSensor(Port.S2)
distance_sensor = InfraredSensor(Port.S4)

#объявляем процедуру отъезда от конвейера (доставка платы в красный квадрат)
def otezd():
    state = True
    gyro.reset_angle(0)
    block.light.on(Color.RED)

    #переход в режим ожидания до момента пока в кузове не будет заготовки
    #после тогок как мы убедимся что сигнал это не флктуация мы запускаем вращательный мотор
    while state:
        if (distance_sensor.distance() < 20):
            wait(10)
            if (distance_sensor.distance() < 20):
                block.light.on(Color.GREEN)
                steering.run(500)

                #вращаем мотор до того как не провернем робота на 80 градусов
                while (gyro.angle() > -80):
                    pass
                steering.stop()
                ride_staight(True, False)
                state = False

#объявляем процедуру  подъеезда к конвейеру
def podezd():
    state = True
    gyro.reset_angle(0)
    block.light.on(Color.RED)

    #переход в режим ожидания до момента пока из кузова не будет убрана заготовка
    #после тогок как мы убедимся что сигнал это не флктуация мы запускаем вращательный мотор
    while state:
        if (distance_sensor.distance() > 20):
            wait(10)
            if (distance_sensor.distance() > 20):
                block.light.on(Color.GREEN)
                ride_staight(True, True)
                steering.run(-500)
                timeout = False

                #вращаем до того как не провернем робота на 80 градусов
                while (gyro.angle() < 80):
                    pass
                steering.stop()
                state = False

#функция езды по прямой линии с корректировкой направления от датчика гировскопа
def ride_staight(ride, direction):
    #запоминаем начальный угол как 0
    gyro.reset_angle(0)

    #"костыляем" вперед 1 секунду чтобы съехать с линии на которой остановились в прошлый раз
    if (direction == True):
        right_wheel.run(100)
        left_wheel.run(100)
    else:
        right_wheel.run(-100)
        left_wheel.run(-100)
    wait(1000)
    right_wheel.stop()
    left_wheel.stop()

    #едем по линии одновременно корректируя свое движение при помощи рулевого колеса
    while (ride == True):
        #block.screen.clear()
        #block.screen.draw_text(0, 40, gyro.angle())
        #block.screen.draw_text(0, 60, line_sensor.reflection())
        if (gyro.angle() < 0):
          steering.run(30 * gyro.angle())
        if (gyro.angle() > 0):
            steering.run(30 * gyro.angle())
        if (gyro.angle() == 0):

            #выбор наплавления прямого движения в зависимости от того куда нам надо вперед или назад
            if (direction == True):
                right_wheel.run(100)
                left_wheel.run(100)
            else:
                right_wheel.run(-100)
                left_wheel.run(-100)  

        #если мы доехали до черной линии до прерываем функцию движения вперед       
        if (line_sensor.reflection() < 35):
            ride = False
            left_wheel.stop()
            right_wheel.stop()
            steering.stop()

#для декораций рисуем и говрим что-то
block.speaker.set_speech_options("en", "f5", 10, 50)
block.speaker.say("OOKBP BOT")
block.screen.draw_text(25, 0, "Mechanism 2")
block.screen.draw_text(30, 20, "Delivery bot")

#повторяем доставку и возврат к конвейеру 3 раза и на экране отписываем сколько раз доставили плату
for i in range(4):
    otezd()
    block.screen.draw_text(i * 20, 40, i + 1)
    podezd()

#завершаем программу
block.speaker.say("Finished")
wait(3000)

#мини-словарик для обращений к железу
#    block.speaker.beep(420, 200)
#    block.speaker.set_speech_options("en", "f5", 10, 50)
#    block.speaker.say("OOKBP BOT")
#    wait(1000)
#    print("Hello World!")
#    left_wheel.run_angle(100, 1000, wait = True)
#    right_wheel.run_angle(100, 1000, wait = True)
#    steering.run_angle(100, 100, wait = True)
#    current_color = line_sensor.color()
#    current_reflection = line_sensor.reflection()   
#    current_angle = gyro.angle()
#    current_distance = distance_sensor.distance()   
#    block.screen.draw_text(25, 0, "Mechanism 2")
#    block.screen.draw_text(30, 20, "Delivery bot")
#    block.light.on(Color.RED)