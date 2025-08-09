import peewee
from nicegui import ui

import feeder
import ui_common
import ui_main
from db_cat import DbCat
from meowton import meowton


@ui.page('/feeder')
def feeder_page():
    ui.page_title("Meowton | Feeder settings")

    ui_common.header("Feeder settings")

    with ui.row():
        with ui.card():
            ui.label("Servo center").classes('text-primary text-bold')

            ui.label("Center pulse width:")
            stop_pulsewidth = ui.slider(min=feeder.SERVO_MIN, max=feeder.SERVO_MAX, step=10,
                                  value=meowton.feeder.stop_pulsewidth).props("label")

        with ui.card():
            ui.label("Feed amount").classes('text-primary text-bold')

            ui.label("Speed and direction:")
            feed_pulsewidth = ui.slider(min=feeder.SERVO_MIN, max=feeder.SERVO_MAX, step=10,
                                  value=meowton.feeder.feed_pulsewidth).props("label")

            feed_time = ui.number(label="Feed time (mS)", value=meowton.feeder.feed_time)

            with ui.card_actions():
                ui.button("Test", on_click=lambda: meowton.feeder.run_motor(feed_pulsewidth.value, feed_time.value))

        with ui.card():
            ui.label("Detection").classes('text-primary text-bold')

            empty_weight = ui.number(label="Minimum weight (g)", min=0,precision=2, value=meowton.feeder.empty_weight)
            retry_timeout = ui.number(label="Drop time (mS)", min=0,precision=0, value=meowton.feeder.retry_timeout)
            retry_max = ui.number(label="Retries", min=0,precision=0, value=meowton.feeder.retry_max)

        with ui.card():
            ui.label("Anti jamming").classes('text-primary text-bold')

            ui.label("Speed and direction:")
            reverse_pulsewidth = ui.slider(min=feeder.SERVO_MIN, max=feeder.SERVO_MAX, step=10,
                                     value=meowton.feeder.reverse_pulsewidth).props("label")

            reverse_time = ui.number(label="Reverse time (mS)", value=meowton.feeder.reverse_time)

            with ui.card_actions():
                ui.button("Test", on_click=lambda: meowton.feeder.run_motor(reverse_pulsewidth.value, reverse_time.value))

    def save():
        meowton.feeder.feed_pulsewidth = feed_pulsewidth.value
        meowton.feeder.feed_time = feed_time.value
        meowton.feeder.stop_pulsewidth = stop_pulsewidth.value
        meowton.feeder.reverse_pulsewidth = reverse_pulsewidth.value
        meowton.feeder.reverse_time = reverse_time.value

        meowton.feeder.empty_weight=empty_weight.value
        meowton.feeder.retry_timeout=retry_timeout.value
        meowton.feeder.retry_max=retry_max.value
        meowton.feeder.save()
        ui.notify("saved")
        ui.navigate.back()

    ui.button(icon="save", on_click=save)
    ui_common.footer()
