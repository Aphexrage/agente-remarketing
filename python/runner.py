# Esse arquivo deve ser usado para facilitar o run do streamlit
# Ao inves de ficar digitando no terminal, so precisa dar run

import sys
from streamlit.web import cli as stcli

sys.argv = ["streamlit", "run", "./Python/app.py"]
sys.exit(stcli.main())  