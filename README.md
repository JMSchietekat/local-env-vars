# Local Environment Variables

This package allows you to specify which environmental variable you require in your application. It will create a `.env` file, prompt you to populate it, and add the `.env` file to your `.gitignore` file.

The functionality described is in line with the guidelines set out in the [The Twelve-Factor App](https://12factor.net/) section [III Config](https://12factor.net/config). 

## Implementation

```python
from local_env_vars.env import LocalEnvVars

env = LocalEnvVars("sql_server_address", "sql_username", "sql_password")

connection_string = "Driver={{SQL Server}};Server={0}; Database=AdventureWorks;uid={1};pwd={2}".format(
        env.vars['sql_server_address'], env.vars['sql_username'], env.vars['sql_password']
    )
```

Running this code for the first time will create an `.env` and add `.env` to the project `.gitignore` file. 

The `.env` file will have the following content. It will throw an exception reporting that you must provide values to the keys.

`{"sql_server_address": "", "sql_username": "", "sql_password": ""}`

After you have populated the keys with values you will be able to execute the code without any exceptions.
