import displayio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label
from adafruit_matrixportal.matrix import Matrix

from config import config

class TrainBoard:
    """
        get_new_data is a function that is expected to return an array of dictionaries like this:

        [
            {
                'line_color': 0xFFFFFF,
                'destination': 'Dest Str',
                'arrival': '5'
            }
        ]
    """
    def __init__(self, get_new_data):
        self.get_new_data = get_new_data
        self.display = Matrix().display
        self.parent_group = displayio.Group(scale=1, x=0, y=3)

        self.heading_label = Label(config['font'], anchor_point=(0,0))
        self.heading_label.color = config['heading_color']
        self.heading_label.text=config['heading_text']
        self.parent_group.append(self.heading_label)

        self.trains = []
        for i in range(config['num_trains']):
            self.trains.append(Train(self.parent_group, i))

        self.display.show(self.parent_group)

    def refresh(self) -> bool:
        print('Refreshing train information...')
        train_data = self.get_new_data()
        if train_data is not None:
            print('Reply received.')
            for i in range(config['num_trains']):
                if i < len(train_data):
                    train = train_data[i]
                    self._update_train(i, train['line_color'], train['destination'], train['arrival'])
                else:
                    self._hide_train(i)
            print('Successfully updated.')
        else:
            print('No data received. Clearing display.')

            for i in range(config['num_trains']):
                self._hide_train(i)

    def _hide_train(self, index: int):
        self.trains[index].hide()

    def _update_train(self, index: int, line_color: int, destination: str, minutes: str):
        self.trains[index].update(line_color, destination, minutes)

    def turn_off_display(self):
        self.display.brightness = 0

    def turn_on_display(self):
        self.display.brightness = 1

class Train:
    def __init__(self, parent_group, index):
        y = (int)(config['character_height'] + config['text_padding']) * (index + 1)

        self.line_rect = Rect(0, y-3, config['train_line_width'], config['train_line_height'], fill=config['loading_line_color'])

        self.destination_label = Label(config['font'], anchor_point=(0,0))
        self.destination_label.x =  config['train_line_width'] + 1
        self.destination_label.y = y
        self.destination_label.color = config['text_color']
        self.destination_label.text = config['loading_destination_text'][:config['destination_max_characters']]

        self.min_label = Label(config['font'], anchor_point=(0,0))
        self.min_label.x = config['matrix_width'] - (config['min_label_characters'] * config['character_width']) + 1
        self.min_label.y = y
        self.min_label.color = config['text_color']
        self.min_label.text = config['loading_min_text']

        self.group = displayio.Group(scale=1, x=0, y=0)
        self.group.append(self.line_rect)
        self.group.append(self.destination_label)
        self.group.append(self.min_label)

        parent_group.append(self.group)

    def show(self):
        self.group.hidden = False

    def hide(self):
        self.group.hidden = True

    def set_line_color(self, line_color: int):
        self.line_rect.fill = line_color

    def set_destination(self, destination: str):
        self.destination_label.text = destination[:config['destination_max_characters']]

    def set_arrival_time(self, minutes: str):
        # Ensuring we have a string
        minutes = str(minutes)
        minutes_len = len(minutes)

        # Left-padding the minutes label
        minutes = ' ' * (config['min_label_characters'] - minutes_len) + minutes

        self.min_label.text = minutes

    def update(self, line_color: int, destination: str, minutes: str):
        self.show()
        self.set_line_color(line_color)
        self.set_destination(destination)
        self.set_arrival_time(minutes)
