# ecomplus-find-profile
Python script for return profile id for recommendation system

# Technology stack
+ [Python 3](https://www.python.org/downloads/release/python-370/) 
+ [PIP](https://pypi.org/project/pip/)
+ [pandas](https://pandas.pydata.org/) 

# Setting up
Installing dependencies on RHEL based Linux:

```bash
sudo yum install python27 python27-devel python-pip
pip install pandas

## Running the script
```bash
python3 find_profile.py birth_date.year gender addresses[].country_code
```
