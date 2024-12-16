import json
import os
import shutil
import pandas


class DB_Arch:
    def __init__(self, file, folder_name):
        self.file = file
        self.folder_name = folder_name
        self.main_hash_table = {}
        self.name_search_hash_table = {}
        self.phone_search_hash_table = {}
        self.table = []
        self.open_db()

    def load_from_backup(self):
        try:
            with open(f'backup/{self.file}', 'r') as file:
                self.main_hash_table = {}
                self.main_hash_table = json.load(file)
            for key, value in self.main_hash_table.items():
                self.add(key, value["name"], value["phone"], value["dob"])

            with open(f'backup/{self.folder_name}/name_search.json', 'r') as file:
                self.name_search_hash_table = {}
                self.name_search_hash_table = json.load(file)

            with open(f'backup/{self.folder_name}/phone_search.json', 'r') as file:
                self.phone_search_hash_table = {}
                self.phone_search_hash_table = json.load(file)

            with open(self.file, 'w') as file:
                json.dump(self.main_hash_table, file)
            try:
                os.mkdir(self.folder_name)
            except FileExistsError:
                pass
            with open(self.folder_name + '/phone_search.json', 'w') as file:
                json.dump(self.phone_search_hash_table, file)
            with open(self.folder_name + '/name_search.json', 'w') as file:
                json.dump(self.name_search_hash_table, file)
            #print("Success", "DB was loaded from backup successfuly!")
        except FileExistsError or FileNotFoundError: \
                print("Error", "Can not restore from backup")

    def open_db(self):
        try:
            with open(self.file, 'r') as file:
                self.main_hash_table = json.load(file)
            for key, value in self.main_hash_table.items():
                print(key, value['name'], value['phone'], value['dob'])

            with open(self.folder_name + '/name_search.json', 'r') as file:
                self.name_search_hash_table = json.load(file)
            with open(self.folder_name + '/phone_search.json', 'r') as file:
                self.phone_search_hash_table = json.load(file)
        except AttributeError:
            print("DB is not exist", "DB file or folder does not exist! Create in first.")
        except FileNotFoundError:
            print("DB is not exist", "DB file or folder does not exist! Create in first.")

        # self.create_db()

    def create_db(self):
        with open(self.file, 'w') as file:
            json.dump(self.main_hash_table, file)
        try:
            os.mkdir(self.folder_name)
        except FileExistsError:
            pass
        with open(self.folder_name + '/phone_search.json', 'w') as file:
            json.dump(self.phone_search_hash_table, file)
        with open(self.folder_name + '/name_search.json', 'w') as file:
            json.dump(self.name_search_hash_table, file)

    def del_db(self):
        try:
            os.remove(self.folder_name + '/phone_search.json')
            os.remove(self.folder_name + '/name_search.json')
            os.remove(self.file)
            self.main_hash_table = {}
            self.name_search_hash_table = {}
            self.phone_search_hash_table = {}
            print("Success", "Deleted successfully")
        except FileNotFoundError:
            print("Not exist", "Files does not exist")

    def save_db(self):
        try:
            with open(self.file, 'w') as file:
                json.dump(self.main_hash_table, file)
            with open(self.folder_name + '/phone_search.json', 'w') as file:
                json.dump(self.phone_search_hash_table, file)
            with open(self.folder_name + '/name_search.json', 'w') as file:
                json.dump(self.name_search_hash_table, file)
            print("Saved", "DB was successfully saved!")
        except FileNotFoundError:
            print("Error", "DB was deleted. Can not save")

    def create_backup(self):
        try:
            try:
                os.mkdir('backup')
            except FileExistsError:
                pass
            backup_dir_name = 'backup/'
            try:
                dest_dir = os.path.join('backup', os.path.basename(self.folder_name))
                shutil.copytree(self.folder_name, dest_dir)
            except FileExistsError:
                pass
            with open(backup_dir_name + self.file, 'w') as file:
                json.dump(self.main_hash_table, file)
            with open(backup_dir_name + self.folder_name + '/phone_search.json', 'w') as file:
                json.dump(self.phone_search_hash_table, file)
            with open(backup_dir_name + self.folder_name + '/name_search.json', 'w') as file:
                json.dump(self.name_search_hash_table, file)
            print("Success!", "DB saved into backup")
        except FileNotFoundError:
            print("Error", "DB was deleted. Can not save to backup")

    def to_xlsx(self):
        pandas.read_json(self.file).to_excel(f'{self.file}.xlsx')

    def find(self, value):
        if type(value) == int:
            print([value, self.main_hash_table.get(str(value))])

        elif type(value) == str:
            id_employees = self.name_search_hash_table.get(value)
            if id_employees is not None:
                for id in id_employees:
                    print([id, self.main_hash_table.get(str(id))])

        elif type(value) == float:
            id_employees = self.phone_search_hash_table.get(str(value))
            if id_employees is not None:
                for id in id_employees:
                    print([id, self.main_hash_table.get(str(id))])
        else:
            print("There are not attribute with this type")

    def add(self, id_employee, name, phone, dob):
        if self.main_hash_table.get(str(id_employee)) is None:
            self.main_hash_table[str(id_employee)] = {'name': name, 'phone': phone, 'dob': dob}
            try:
                self.name_search_hash_table[name].append(str(id_employee))
            except KeyError:
                self.name_search_hash_table[name] = [str(id_employee)]
            try:
                self.phone_search_hash_table[str(phone)].append(str(id_employee))
            except KeyError:
                self.phone_search_hash_table[str(phone)] = [str(id_employee)]

        else:
            print("Not unique value", "Can not add object with not unique value of key attribute")

    def del_value(self, value):
        # try:

        if type(value) == int:
            self.name_search_hash_table[self.main_hash_table[str(value)]['name']].remove(str(value))
            self.phone_search_hash_table[str(self.main_hash_table[str(value)]['phone'])].remove(str(value))
            del self.main_hash_table[str(value)]

        elif type(value) == str:
            for id_employee in self.name_search_hash_table[value]:
                self.phone_search_hash_table[str(self.main_hash_table[id_employee]['phone'])].remove(id_employee)
            for id_employee in self.name_search_hash_table[value]:
                del self.main_hash_table[id_employee]
            del self.name_search_hash_table[str(value)]
        elif type(value) == float:
            for id_employee in self.phone_search_hash_table[str(value)]:
                self.name_search_hash_table[self.main_hash_table[id_employee]['name']].remove(id_employee)
            for id_employee in self.phone_search_hash_table[str(value)]:
                del self.main_hash_table[id_employee]
            del self.phone_search_hash_table[str(value)]
        else:
            print("There are not attribute with this type")
        # except KeyError:
        #     print("There are not this value in DB")

    def editing(self, id_employee, name, phone, dob):
        if [type(id_employee), type(name), type(phone), type(dob)] == [int, str, float, bool]:
            if self.main_hash_table.get(str(id_employee)) is not None:
                print("in editing")
                try:
                    self.name_search_hash_table[name].append(str(id_employee))
                except KeyError:
                    self.name_search_hash_table[name] = [str(id_employee)]
                try:
                    self.phone_search_hash_table[str(phone)].append(str(id_employee))
                    print("yessssss")
                except KeyError:
                    self.phone_search_hash_table[str(phone)] = [str(id_employee)]
                self.name_search_hash_table[self.main_hash_table[str(id_employee)]['name']].remove(str(id_employee))
                self.phone_search_hash_table[str(self.main_hash_table[str(id_employee)]['phone'])].remove(
                    str(id_employee))
                self.main_hash_table[str(id_employee)]['dob'] = dob
                self.main_hash_table[str(id_employee)]['name'] = name
                self.main_hash_table[str(id_employee)]['phone'] = phone
                # except KeyError:
                #    print("Error", "There are not this value in DB")
        else:
            print("Error", "Wrong input type!")
