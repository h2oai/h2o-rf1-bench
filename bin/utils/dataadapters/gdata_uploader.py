#!/usr/bin/python

import time, os.path
import gdata.gauth
import gdata.spreadsheets.client
import argparse

__author__ = 'michal.malohlava@gmail.com (Michal  Malohlava)'

USER_AGENT          = 'BenchDataAdapter'
DEFAULT_SECRET_FILE = '.bda_secrets'

DEFAULT_SPREADSHEET_KEY = '0AoSStNWp5_DSdGVfc0VJYVBKUWpoZE9XOFlMaC1hLXc'
DEFAULT_WORKSHEET_ID    = 'od6'

CLIENT_ID     = '876823250318.apps.googleusercontent.com'
CLIEND_SECRET = 'fKGPV_rxYa-HqTcKG71EWfSE' 
REDIRECT_URI  = 'urn:ietf:wg:oauth:2.0:oob'

DEFAULT_SCOPES = ['https://spreadsheets.google.com/feeds/']

DEFAULT_COLUMNS= {
        'A': 'date',
        'B': 'tool'
        'C': 'dataset',
        'D': 'ntree',
        'E': 'mtry',
        'F': 'leave_min',
        'G': 'leave_mean',
        'H': 'leave_max',
        'I': 'depth_min',
        'J': 'depth_mean',
        'K': 'depth_max',
        'L': 'train_size',
        'M': 'oobee',
        'N': 'test_size',
        'O': 'class_error',
        'P': 'sampling_rage',
        'Q': 'cmd_line',
        'R': 'notes'
        }

class GDataAdapter:
    """Simple class uploading given data into a given spreadsheet."""

    def __init__(self, authorize=True, client_id=CLIENT_ID, client_secret=CLIEND_SECRET, scopes=DEFAULT_SCOPES, user_agent=USER_AGENT, verbose=False):

        self.client       = None
        self.verbose      = verbose

        if (authorize):
            self.auth(client_id,client_secret,scopes,user_agent)

# 
# PRIVATE PART
#
    def _verify(self, client_id, client_secret, scopes, user_agent):
        token = gdata.gauth.OAuth2Token(client_id=client_id, 
                                        client_secret=client_secret,
                                        scope=' '.join(scopes),
                                        user_agent=user_agent)

        print """
=============================================
Please vist the following URL
and allow this application to access your spreadsheets:
%s
=============================================
""" %  (token.generate_authorize_url() )
        code = raw_input('What is the verification code? ').strip()
        token.get_access_token(code)
        print token.access_token
        print token.refresh_token

        return token

    def _is_secretfile_exists(self, f=DEFAULT_SECRET_FILE):
        return os.path.exists(f)

    def _load_tokens(self, file_name=DEFAULT_SECRET_FILE):
        """Returns a pair of access and refresh tokens, or (None,None) if the tokens cannot be loaded"""
        if not os.path.exists(file_name):
            return (None, None)
        
        with open(file_name, 'r') as f:
            access_token  = f.readline().rstrip('\n')
            refresh_token = f.readline().rstrip('\n')

        if access_token == "":
            access_token = None
        if refresh_token == "":
            refresh_token = None

        return (access_token, refresh_token)

    def _save_tokens(self, access_token, refresh_token, file_name=DEFAULT_SECRET_FILE):
        with open(file_name, 'w') as f:
            f.write(access_token)
            f.write('\n')
            f.write(refresh_token)
            f.write('\n')

    def _auth(self, client_id, client_secret, scopes, user_agent, access_token, refresh_token):
       
        token = gdata.gauth.OAuth2Token(client_id=client_id, 
                                        client_secret=client_secret,
                                        scope=' '.join(scopes),
                                        user_agent=user_agent,
                                        access_token=access_token,
                                        refresh_token=refresh_token)

        return token

    def _getclient(self):
        if self.client is None:
            #self.client = gdata.spreadsheet.service.SpreadsheetsService()
            self.client = gdata.spreadsheets.client.SpreadsheetsClient()
            self._token.authorize(self.client)        

    def _print_feed(self, feed):
        for i, entry in enumerate(feed.entry):
            eid     = entry.id.text.rsplit('/',1)[1]
            etitle  = entry.title.text
            if etitle is not None:
                etitle = etitle.encode('utf-8')
            eauthors = self._list_authors(entry)
            if eauthors:
                eauthors = " ({0})".format(','.join(eauthors).encode('utf-8'))
            else:
                eauthors = ""

            print "{0}: '{1}'{2} [id: {3}] \n".format(i, etitle, eauthors, eid)
            self._verbose(entry, "Feed entry:")

    def _list_authors(self, entry):
        authors = []
        for i, author in enumerate(entry.author):
            authors.append(author.name.text)
        
        return authors

    def _verbose(self, entry, premsg, postmsg=None):
        if self.verbose:
            print premsg
            print entry
            print postmsg
            print 


# 
# PUBLIC PART
#

    def setVerbose(self, yes=True):
        self.verbose = yes

    def auth(self, client_id, client_secret, scopes, user_agent):
        # load tokens
        (access_token, refresh_token) = self._load_tokens()
        if (access_token == None or refresh_token == None):
            token = self._verify(client_id, client_secret, scopes, user_agent)
            # save retrieved tokens
            self._save_tokens(token.access_token, token.refresh_token)
        else:
            token = self._auth(client_id, client_secret, scopes, user_agent, access_token, refresh_token)
            print "Is invalid: "
            print token.invalid

        self._token = token
        
        # Setup Google Data client and authorize it.
        self._getclient()

    def insertCSVData(header, csv_data):
        for row in data:
            entry = self.client.InsertRow(row, self.spreadsheet_key, self.worksheet_id)

    def listSpreadsheets(self, printit=True):
        spreadsheets = self.client.GetSpreadsheets()
        if printit:
            self._print_feed(spreadsheets)
        return spreadsheets

    def listTables(self, spreadsheet_key, printit=True):
        tables = self.client.GetTables(spreadsheet_key,id='ss6')
        if printit:
            self._print_feed(tables)
        return tables

    def listWorksheets(self, spreadsheet_key, printit=True):
        worksheets = self.client.GetWorksheets(spreadsheet_key)
        if printit:
            self._print_feed(worksheets)
        return worksheets

    def addTableForTool(self, spreadsheet_key, tool_name, columns=DEFAULT_COLUMNS, table_title=None, table_desc=None, header_row=1, num_rows=0, start_row=2, insertion_mode='insert' ):
        if table_desc is None:
            table_desc = "Table for %s benchmarks" % (tool_name)
        if table_title is None:
            table_title = "%s benchmarks" % (tool_name)

        worksheet_name = tool_name
        
        table = self.client.AddTable(spreadsheet_key, 
                table_title, 
                table_desc, 
                worksheet_name, 
                header_row, 
                num_rows, 
                start_row, 
                insertion_mode, 
                columns)

        self._verbose(table, "Result of AddTable call:")

        return table

    def _find_by_id(self, feed, rid):
        for i, entry in enumerate(feed.entry):
            eid = entry.id.text.rsplit('/',1)[1]
            if eid == rid:
                return entry

        return None

    def getTable(self, spreadsheet_key, table_id):
        tables = self.listTables(spreadsheet_key, printit=False)
        table = self._find_by_id(tables, table_id)

        return table
           
    def deleteTable(self, spreadsheet_key, table_id):
        table = self.getTable(spreadsheet_key, table_id)
        if table:
            self.client.delete(table)
            return True
        else:
            return False

    def listRecords(self, spreadsheet_key, table_id, printit=True):
        records = self.client.GetRecords(spreadsheet_key, table_id)
        if printit:
            self._print_feed(records)
        return records
    
    def addRecord(self, spreadsheet_key, table_id, record):
        row = dict_from_csv_record(record) 
        table = self.client.AddRecord(spreadsheet_key, table_id, row)
        print table

    def is_authorized(self):
        return self._token is not None

def dict_from_csv_record(record):
    res = {}
    cnt = 0
    items = record.split(',')
    if len(items) > 0:
        for (c,col) in DEFAULT_COLUMNS.items():
            if cnt < len(items):
                res[col] = items[cnt]
            else:
                res[col] = 'N/A'
            cnt = cnt + 1

    return res

def main():
    parser = argparse.ArgumentParser(description="GData Benchmark Adapter")
    parser.add_argument('spreadsheet', type=str, nargs='?', help="spreadsheet key (by default {0} is used)".format(DEFAULT_SPREADSHEET_KEY), default=DEFAULT_SPREADSHEET_KEY)
    parser.add_argument('--list_spreadsheets', help="list all spreadsheets", action="store_true")
    parser.add_argument('--list_tables', help="list all tables", action="store_true")
    parser.add_argument('--list_worksheets', help="list all worksheets stored in given spreadsheet (specified by key)", action="store_true")
    
    parser.add_argument('--add_table', type=str, help="add a new default table for given tool", metavar='table_name')
    parser.add_argument('--delete_table', type=str, help="delete table specified by table_id", metavar='table_id')
    parser.add_argument('--list_records', type=str, help="list all record in a table", metavar="table_id")

    parser.add_argument('--add_record', type=str, help="add a record into the given table. Items in cvs_record are separated by commas.", metavar=('table_id','cvs_record'), nargs=2)

    parser.add_argument('-v', '--verbose', help="be more verbosed", action="store_true")

    args = parser.parse_args()

    adapter = GDataAdapter()
    # Configure adapter
    if args.verbose:
        adapter.setVerbose()

    # Execute action
    if args.list_tables:
        print "List of tables in spreadsheet id:{0}:".format(args.spreadsheet)
        adapter.listTables(args.spreadsheet)
    elif args.list_spreadsheets:
        print "List of spreadsheets:"
        adapter.listSpreadsheets()
    elif args.list_worksheets:
        print "List of worksheets in spreadsheet id:{0}:".format(args.spreadsheet)
        adapter.listWorksheets(args.spreadsheet)
    elif args.add_table is not None:
        print "Adding table {0} into spreadsheet id:{1}".format(args.add_table, args.spreadsheet)
        table = adapter.addTableForTool(args.spreadsheet, args.add_table)
        if isinstance(table, gdata.spreadsheets.data.Table):
            print "Table create with id: {0}".format(table.get_table_id())
        else:
            print "Table was not created!"
            print "Call of AddTable method returned:"
            print table
    elif args.delete_table is not None:
        print "Deleting table with id:{0} from spreadsheet id:{1}".format(args.delete_table, args.spreadsheet)
        result = adapter.deleteTable(args.spreadsheet, args.delete_table)
        print result
    elif args.list_records is not None:
        print "Listing records from table with id:{0} from spreadsheet id:{1}".format(args.list_records, args.spreadsheet)
        result = adapter.listRecords(args.spreadsheet, args.list_records)
    elif args.add_record is not None:
        print "Adding a new row into table id:{0} from spreadsheet id:{1}".format(args.add_record[0], args.spreadsheet)
        result = adapter.addRecord(args.spreadsheet, args.add_record[0], args.add_record[1])
    else:
        print "No action specified...exiting..."

if __name__ == '__main__':
  main()
