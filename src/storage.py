# from dataclasses import dataclass
import psycopg2


class Storage:
    # psql -h 193.219.42.55 -p 2391 -d pullout -U admin
    def __init__(self):
        self.conn = psycopg2.connect(
            host="193.219.42.55",
            port=2391,
            database="pullout",
            user="admin",
            password="password")
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def print_all(self):
        self.cur.execute('SELECT * FROM card')
        results = self.cur.fetchall()
        for result in results:
            print(result)

    def get_all(self):
        self.cur.execute('SELECT * FROM card')
        results = self.cur.fetchall()
        return results

    def delete_by_id(self):
        delete_tbl_data = "DELETE FROM card WHERE id = '1';"
        self.cur.execute(delete_tbl_data)

    def find_by_id(self):
        self.cur.execute('SELECT * FROM card WHERE id = "1"')
        results = self.cur.fetchall()
        return results

    def find_by_person(self, person):
        self.cur.execute('SELECT * FROM card WHERE fullname = "person"')
        results = self.cur.fetchall()
        return results

    def insert_row(self):
        sql = '''INSERT INTO card(company, person, role, phone, email, website)
        VALUES ('abc_company2', 'abc_person2', 'abc_role2', 'abc_phone2', 'abc_email2', 'abc_website2');'''

        # executing the sql statement
        self.cur.execute(sql)

        # committing the changes
        self.conn.commit()

    def list_items(self):
        self.cur.execute('SELECT * FROM card')
        results = self.cur.fetchall()
        print(results)

    def add(self, storage_entry):
        company = None
        person = None
        role = None
        phone = None
        email = None
        website = None

        if 'person' in storage_entry:
            person = storage_entry['person']

        if "phones" in storage_entry:
            phones = storage_entry['phones']
            if len(phones):
                phone = phones[0]

        if "jobs" in storage_entry:
            jobs = storage_entry['jobs']
            if len(jobs):
                role = jobs[0]

        if "org" in storage_entry:
            org = storage_entry['org']
            if len(org):
                company = org[0]

        if "emails" in storage_entry:
            emails = storage_entry['emails']
            if len(emails):
                email = emails[0]

        if "websites" in storage_entry:
            websites = storage_entry['websites']
            if len(websites):
                website = websites[0]

        sql = f'''INSERT INTO card(company, person, role, phone, email, website)
        VALUES ( '{company}', '{person}', '{role}', '{phone}', '{email}', '{website}')'''

        self.cur.execute(sql)
        self.conn.commit()



    #
    # def remove_by_name(self, name: str):
    #     pass


# storage = Storage()
# storage.insert_row()
# storage.print_all()