# proj6-mongo
Simple list of dated memos kept in MongoDB database, users can add memos as well as delete them

Author: Holden Oullette

## Installation & Deployment ##

```bash
git clone https://github.com/houllette/proj6-mongo
cd proj6-mongo
./configure
```

From here, you need to install MongoDB and create and Admin user. Assuming you have done this,
put Admin credentials inside of secrets/admin_secrets.skel and change the filetype to py.

Do the same file change to client_secrets.skel and input your desired credentials.

In the project's root directory:
```bash
python3 create_db.py
source env/bin/activate
make run
```

## Testing ##
```bash
source env/bin/activate
make test
```