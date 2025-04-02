from django.db import models

# Create your models here.
class Voter(models.Model):
    '''
    Model to store/represent the data of registered voters in Newton, MA
    '''
    # identification
    first_name = models.TextField()
    last_name = models.TextField()
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.IntegerField()
    date_of_birth = models.TextField()
    date_of_registration = models.TextField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=2)

    # fields to indicate whether or not a given voter participated in several recent elections
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    # voter score
    voter_score = models.IntegerField()


    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}'

def load_data():
    '''Method to load and store the csv file into the database'''
    # very dangerous!
    # Voter.objects.all().delete()

    filename = '/Users/lancesinson/Desktop/newton_voters.csv'

    f = open(filename, 'r')
    f.readline()

    for line in f:

        try:
            fields = line.strip().split(',')

            voter = Voter(
                    first_name = fields[2],
                    last_name = fields[1],
                    street_number = fields[3],
                    street_name = fields[4],
                    apartment_number = fields[5],
                    zip_code = fields[6],
                    date_of_birth = fields[7],
                    date_of_registration = fields[8],
                    # party_affiliation = fields[9],
                    party_affiliation = fields[9].strip(),
                    precinct_number = fields[10],

                    v20state = (fields[11].strip().upper() == 'TRUE'),
                    v21town = (fields[12].strip().upper() == 'TRUE'),
                    v21primary = (fields[13].strip().upper() == 'TRUE'),
                    v22general = (fields[14].strip().upper() == 'TRUE'),
                    v23town = (fields[15].strip().upper() == 'TRUE'),


                    voter_score = fields[16]
                    )

            voter.save() # commit this voter to the database

 
        except:
            print("Something went wrong!")
            print(f"line={line}")


    print(f"Done. Created {len(Voter.objects.all())} Results")



        # ['05SJR0784000', 'SKARIE', 'JENNIFER', '571', 'COMMONWEALTH AVE', '', '02459', '1984-05-07', '2021-07-16', 'D ', '2', 'FALSE', 'FALSE', 'FALSE', 'TRUE', 'TRUE', '2']
        # fields[0] = 05SJR0784000
        # fields[1] = SKARIE
        # fields[2] = JENNIFER
        # fields[3] = 571
        # fields[4] = COMMONWEALTH AVE
        # fields[5] = 
        # fields[6] = 02459
        # fields[7] = 1984-05-07
        # fields[8] = 2021-07-16
        # fields[9] = D 
        # fields[10] = 2
        # fields[11] = FALSE
        # fields[12] = FALSE
        # fields[13] = FALSE
        # fields[14] = TRUE
        # fields[15] = TRUE
        # fields[16] = 2

        # show which value in each field
        # print(fields)
        # for j in range(len(fields)):
        #     print(f'fields[{j}] = {fields[j]}')

        