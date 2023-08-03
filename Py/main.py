import json
import os
import datetime

class Note:
    def __init__(self, note_id, title, body):
        self.note_id = note_id
        self.title = title
        self.body = body
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def update(self, title, body):
        self.title = title
        self.body = body
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        return {
            "note_id": self.note_id,
            "title": self.title,
            "body": self.body,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class NotesManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.file_path, 'r') as file:
                notes_data = json.load(file)
                notes = [Note(note["note_id"], note["title"], note["body"]) for note in notes_data]
                return notes
        except FileNotFoundError:
            return []

    def save_notes(self):
        notes_data = [note.to_dict() for note in self.notes]
        with open(self.file_path, 'w') as file:
            json.dump(notes_data, file)

    def create_note(self, title, body):
        max_id = max([note.note_id for note in self.notes], default=0)
        note_id = max_id + 1
        new_note = Note(note_id, title, body)
        self.notes.append(new_note)
        self.save_notes()
        print("Заметка успешно создана.")

    def read_notes(self):
        if not self.notes:
            print("Список заметок пуст.")
        else:
            for note in self.notes:
                print(f"{note.note_id}. {note.title}")

    def read_note_content(self, note_id):
        note = self.get_note_by_id(note_id)
        if note:
            print(f"Заголовок: {note.title}")
            print(f"Тело заметки:\n{note.body}")
        else:
            print("Заметки с таким идентификатором не существует.")

    def update_note(self, note_id, title, body):
        note = self.get_note_by_id(note_id)
        if note:
            note.update(title, body)
            self.save_notes()
            print("Заметка успешно обновлена.")
        else:
            print("Заметки с таким идентификатором не существует.")

    def delete_note(self, note_id):
        note = self.get_note_by_id(note_id)
        if note:
            self.notes.remove(note)
            self.save_notes()
            print("Заметка успешно удалена.")
        else:
            print("Заметки с таким идентификатором не существует.")

    def get_note_by_id(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                return note
        return None


def main():
    file_path = 'notes.json'
    notes_manager = NotesManager(file_path)

    while True:
        print("\nВыберите действие:")
        print("1. Создать заметку")
        print("2. Посмотреть список заметок")
        print("3. Посмотреть содержимое заметки")
        print("4. Обновить заметку")
        print("5. Удалить заметку")
        print("0. Выйти")

        choice = input("Введите номер действия: ")

        if choice == '1':
            title = input("Введите заголовок заметки: ")
            body = input("Введите содержимое заметки: ")
            notes_manager.create_note(title, body)

        elif choice == '2':
            notes_manager.read_notes()

        elif choice == '3':
            note_id = int(input("Введите идентификатор заметки: "))
            notes_manager.read_note_content(note_id)

        elif choice == '4':
            note_id = int(input("Введите идентификатор заметки: "))
            title = input("Введите новый заголовок заметки: ")
            body = input("Введите новое содержимое заметки: ")
            notes_manager.update_note(note_id, title, body)

        elif choice == '5':
            note_id = int(input("Введите идентификатор заметки: "))
            notes_manager.delete_note(note_id)

        elif choice == '0':
            break

        else:
            print("Неправильный номер действия. Попробуйте еще раз.")

if __name__ == "__main__":
    main()
