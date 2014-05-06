from comp61542.statistics import average
import itertools
import numpy as np
from xml.sax import handler, make_parser, SAXException
from networkx import Graph, NetworkXError, NetworkXNoPath, shortest_path_length, all_shortest_paths

PublicationType = [
    "Conference Paper", "Journal", "Book", "Book Chapter"]


class Publication:
    CONFERENCE_PAPER = 0
    JOURNAL = 1
    BOOK = 2
    BOOK_CHAPTER = 3

    def __init__(self, pub_type, title, year, authors):
        self.pub_type = pub_type
        self.title = title
        if year:
            self.year = int(year)
        else:
            self.year = -1
        self.authors = authors


class Author:
    def __init__(self, name):
        self.name = name


class Stat:
    STR = ["Mean", "Median", "Mode"]
    FUNC = [average.mean, average.median, average.mode]
    MEAN = 0
    MEDIAN = 1
    MODE = 2


class Database:
    def read(self, filename):
        self.publications = []
        self.authors = []
        self.author_idx = {}
        self.min_year = None
        self.max_year = None

        handler = DocumentHandler(self)
        parser = make_parser()
        parser.setContentHandler(handler)
        infile = open(filename, "r")
        valid = True
        try:
            parser.parse(infile)
        except SAXException as e:
            valid = False
            print "Error reading file (" + e.getMessage() + ")"
        infile.close()

        for p in self.publications:
            if self.min_year == None or p.year < self.min_year:
                self.min_year = p.year
            if self.max_year == None or p.year > self.max_year:
                self.max_year = p.year

        self.authors_graph = self._build_authors_graph()
        return valid

    def get_all_authors(self):
        return self.author_idx.keys()

    def get_all_authors_name(self):
        authors = [self.authors[a].name for a in range(0, len(self.authors))]
        authors.sort()
        return authors

    def get_coauthor_data(self, start_year, end_year, pub_type):
        coauthors = {}
        for p in self.publications:
            if ((start_year == None or p.year >= start_year) and
                    (end_year == None or p.year <= end_year) and
                    (pub_type == 4 or pub_type == p.pub_type)):
                for a in p.authors:
                    for a2 in p.authors:
                        if a != a2:
                            try:
                                coauthors[a].add(a2)
                            except KeyError:
                                coauthors[a] = set([a2])

        def display(db, coauthors, author_id):
            return "%s (%d)" % (db.authors[author_id].name, len(coauthors[author_id]))

        header = ("Author", "Co-Authors")
        data = []
        for a in coauthors:
            data.append([display(self, coauthors, a),
                         ", ".join([
                             display(self, coauthors, ca) for ca in coauthors[a]])])
            # data.append([[self.authors[a].name, display(self, coauthors, a)],
            #              [[self.authors[ca].name, ", ".join([display(self, coauthors, ca)])] for ca in coauthors[a]]])

        return (header, data)

    def get_coauthor_by_author_name(self, name):
        coauthors = set()
        for p in self.publications:
            for a in p.authors:
                if a == self.author_idx[name]:
                    for a2 in p.authors:
                        if a != a2:
                            coauthors.add(a2)

        return (["Co-Authors"], [self.authors[ca].name for ca in coauthors])

    def get_coauthor_graph_by_author_name(self, name):
        coauthors = set()
        for p in self.publications:
            for a in p.authors:
                if a == self.author_idx[name]:
                    for a2 in p.authors:
                        if a != a2:
                            coauthors.add(a2)

        graph = Graph()
        # the nodes format will be {"id":int, "name":str}
        graph.add_node(self.author_idx[name], {"name":name})
        print graph
        # graph.add_nodes_from([(i, {"name": all_data[0][i][0]}) for i in range(len(all_data[0]))])
        graph.add_nodes_from([ca, self.authors[ca].name] for ca in coauthors)
        graph.add_edges_from([(self.author_idx[name], name), (ca, self.authors[ca].name)] for ca in coauthors)

        return graph

    def get_average_authors_per_publication(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [func(auth_per_pub[i]) for i in np.arange(4)] + [func(list(itertools.chain(*auth_per_pub)))]
        return (header, data)

    def get_average_publications_per_author(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))

        for p in self.publications:
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [func(pub_per_auth[:, i]) for i in np.arange(4)] + [func(pub_per_auth.sum(axis=1))]
        return (header, data)

    def get_average_publications_in_a_year(self, av):
        header = ("Conference Paper",
                  "Journal", "Book", "Book Chapter", "All Publications")

        ystats = np.zeros((int(self.max_year) - int(self.min_year) + 1, 4))

        for p in self.publications:
            ystats[p.year - self.min_year][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [func(ystats[:, i]) for i in np.arange(4)] + [func(ystats.sum(axis=1))]
        return (header, data)

    def get_average_authors_in_a_year(self, av):
        header = ("Conference Paper",
                  "Journal", "Book", "Book Chapter", "All Publications")

        yauth = [[set(), set(), set(), set(), set()] for _ in range(int(self.min_year), int(self.max_year) + 1)]

        for p in self.publications:
            for a in p.authors:
                yauth[p.year - self.min_year][p.pub_type].add(a)
                yauth[p.year - self.min_year][4].add(a)

        ystats = np.array([[len(S) for S in y] for y in yauth])

        func = Stat.FUNC[av]

        data = [func(ystats[:, i]) for i in np.arange(5)]
        return (header, data)

    def get_publication_summary_average(self, av):
        header = ("Details", "Conference Paper",
                  "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))
        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        name = Stat.STR[av]
        func = Stat.FUNC[av]

        data = [
            [name + " authors per publication"]
            + [func(auth_per_pub[i]) for i in np.arange(4)]
            + [func(list(itertools.chain(*auth_per_pub)))],
            [name + " publications per author"]
            + [func(pub_per_auth[:, i]) for i in np.arange(4)]
            + [func(pub_per_auth.sum(axis=1))]]
        return (header, data)

    def get_publication_summary(self):
        header = ("Details", "Conference Paper",
                  "Journal", "Book", "Book Chapter", "Total")

        plist = [0, 0, 0, 0]
        alist = [set(), set(), set(), set()]

        for p in self.publications:
            plist[p.pub_type] += 1
            for a in p.authors:
                alist[p.pub_type].add(a)
        # create union of all authors
        ua = alist[0] | alist[1] | alist[2] | alist[3]

        data = [
            ["Number of publications"] + plist + [sum(plist)],
            ["Number of authors"] + [len(a) for a in alist] + [len(ua)]]
        return (header, data)

    def get_average_authors_per_publication_by_author(self, av):
        header = ("Author", "Number of conference papers",
                  "Number of journals", "Number of books",
                  "Number of book chapers", "All publications")

        astats = [[[], [], [], []] for _ in range(len(self.authors))]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [[self.authors[i].name]
                + [func(L) for L in astats[i]]
                + [func(list(itertools.chain(*astats[i])))]
                for i in range(len(astats))]
        return (header, data)


    def get_publications_by_author(self):
        header = ("Author", "Number of conference papers",
                  "Number of journals", "Number of books",
                  "Number of book chapers", "Total", "Last name")

        astats = [[0, 0, 0, 0] for _ in range(len(self.authors))]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type] += 1

        data = [[self.authors[i].name] + astats[i] + [sum(astats[i])] +
                [self.authors[i].name.split(" ")[len(self.authors[i].name.split(" ")) - 1]]
                for i in range(len(astats))]
        return (header, data)

    def get_publication_timeline_by_author_name(self, name):
        """
        gets all detailed publication data (year, title, authors) for 1 particular author.
        the data will be displayed in the form of timeline on author profile page in a cronological order.

        @author 1: dumbastic

        @type  name: String
        @param name: Name of the author. Example: "Author A"

        @rtype:   dict
        @return:  Returns all publication data, in the format of:
                    [(year0,[[title0,author0,author1]]),(year1,[[title1,author1,author2],...,[]]),...,()]
        """
        ystats = {}
        publist = {}

        for p in self.publications:
            for a in p.authors:
                if a == self.author_idx[name]:
                    pub = [p.title]
                    pub.extend([self.authors[i].name for i in p.authors])

                    if p.year in ystats:
                        publist = ystats[p.year]
                    else:
                        publist = list()

                    publist.append(pub)
                    ystats[p.year] = publist

        return sorted(ystats.items(), key=lambda t: t[0], reverse=True)

    def get_author_statistics(self):
        header = ("Author", "Number of \"hands-on\" researches",
                  "Number of projects managed", "Number of other publications", "Total")

        astats = [[0, 0, 0] for _ in range(len(self.authors))]
        for p in self.publications:
            for a in p.authors:
                if a == p.authors[0] or a == p.authors[len(p.authors) - 1]:
                    if a == p.authors[0]:
                        astats[a][0] += 1
                    if a == p.authors[len(p.authors) - 1]:
                        astats[a][1] += 1
                else:
                    astats[a][2] += 1

        data = [[self.authors[i].name] + astats[i] + [sum(astats[i])]
                for i in range(len(astats))]
        return (header, data)

    def get_author_statistics_with_sole(self, pub_type):
        header = ("Author", "First author", "Last author", "Sole author", "Other", "Total", "Last name")

        astats = [[0, 0, 0, 0] for _ in range(len(self.authors))]
        for p in self.publications:
            for a in p.authors:
                if pub_type == 4 or pub_type == p.pub_type:
                    if len(p.authors) == 1:
                        astats[a][2] += 1
                    else:
                        if a == p.authors[0] or a == p.authors[len(p.authors) - 1]:
                            if a == p.authors[0]:
                                astats[a][0] += 1
                            if a == p.authors[len(p.authors) - 1]:
                                astats[a][1] += 1
                        else:
                            astats[a][3] += 1

        data = [[self.authors[i].name] + astats[i] + [sum(astats[i])] +
                [self.authors[i].name.split(" ")[len(self.authors[i].name.split(" ")) - 1]]
                for i in range(len(astats))]
        return (header, data)

    def get_author_statistics_detailed_all(self, name):
        """
        Built on top of get_author_statistics_detailed method, it gets all detailed statistics for one particular
        author with customisation of each publication type name on each data row. (Conference Paper, Journal, Book, Book
        Chapter, All Publication)

        @author 1: CipherHat

        @type  name: String
        @param name: Name of the author. Example: "Author A"

        @rtype:   dict
        @return:  Returns all type of publication data, in the format of: [header,data[[x,y0,y1,y2,y3,y4],[x,y0,y1,y2,y3,y4],...]]
                    x = The string name of publication type e.g: Conference Papers
                    y0 = The number of publications the author appears first
                    y1 = The number of publications the author appears last
                    y2 = The number of publications the author has sole ownership
                    y3 = The number of co-authors for the author
                    y4 = The number of overall publications for the author
        """
        header = ("", "First Author", "Last Author", "Sole Author", "Other", "All", "Co-Authors")
        title = ["Conference Papers", "Journal", "Book", "Book Chapter", "All Publication"]
        data = [[str(title[i])] + self.get_author_statistics_detailed(name, i) for i in range(0, 5)]
        return (header, data)


    def get_author_statistics_detailed(self, name, pub_type):
        """
        Get detailed statistics for one particular author.

        @author 1: Sylvain, Ruvin

        @type  name: String
        @param name: Name of the author. Example: "Author A"
        @type  pub_type: int
        @param pub_type: The publication type ranging from 0-4
                    0 = CONFERENCE PAPER (INPROCEEDINGS)
                    1 = JOURNAL
                    2 = BOOK
                    3 = BOOK CHAPTER
                    4 = ALL PUBLICATION
        @rtype:   dict
        @return:  Ranging from 0-4
                    0 = The number of publications the author appears first
                    1 = The number of publications the author appears last
                    2 = The number of publications the author has sole ownership
                    3 = The number of publications the author appear as co-author
                    4 = The number of overall publications for the author
                    3 = The number of co-authors for the author
        """
        if (pub_type > 4):
            raise ValueError
        author_id = self.author_idx[name]
        data = [0, 0, 0, 0, 0, 0]
        coauthors = []
        for p in self.publications:
            if (pub_type == 4 or p.pub_type == pub_type):
                if author_id in p.authors:
                    for a in p.authors:
                        if a == author_id:
                            data[4] += 1
                            if len(p.authors) == 1 and author_id == p.authors[0]:
                                data[2] += 1
                            else:
                                if author_id == p.authors[0] or author_id == p.authors[len(p.authors) - 1]:
                                    if author_id == p.authors[0]:
                                        data[0] += 1
                                    if author_id == p.authors[len(p.authors) - 1]:
                                        data[1] += 1
                                else:
                                    data[3] += 1
                        else:
                            if not (a in coauthors):
                                coauthors.append(a)
        data[5] = len(coauthors)
        return data

    def get_average_authors_per_publication_by_year(self, av):
        header = ("Year", "Conference papers",
                  "Journals", "Books",
                  "Book chapers", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type].append(len(p.authors))
            except KeyError:
                ystats[p.year] = [[], [], [], []]
                ystats[p.year][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [[y]
                + [func(L) for L in ystats[y]]
                + [func(list(itertools.chain(*ystats[y])))]
                for y in ystats]
        return (header, data)

    def get_publications_by_year(self):
        header = ("Year", "Number of conference papers",
                  "Number of journals", "Number of books",
                  "Number of book chapers", "Total")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type] += 1
            except KeyError:
                ystats[p.year] = [0, 0, 0, 0]
                ystats[p.year][p.pub_type] += 1

        data = [[y] + ystats[y] + [sum(ystats[y])] for y in ystats]
        return (header, data)

    def get_average_publications_per_author_by_year(self, av):
        header = ("Year", "Conference papers",
                  "Journals", "Books",
                  "Book chapers", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year]
            except KeyError:
                s = np.zeros((len(self.authors), 4))
                ystats[p.year] = s
            for a in p.authors:
                s[a][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [[y]
                + [func(ystats[y][:, i]) for i in np.arange(4)]
                + [func(ystats[y].sum(axis=1))]
                for y in ystats]
        return (header, data)

    def get_author_totals_by_year(self):
        header = ("Year", "Number of conference papers",
                  "Number of journals", "Number of books",
                  "Number of book chapers", "Total")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year][p.pub_type]
            except KeyError:
                ystats[p.year] = [set(), set(), set(), set()]
                s = ystats[p.year][p.pub_type]
            for a in p.authors:
                s.add(a)
        data = [[y] + [len(s) for s in ystats[y]] + [len(ystats[y][0] | ystats[y][1] | ystats[y][2] | ystats[y][3])]
                for y in ystats]
        return (header, data)

    def add_publication(self, pub_type, title, year, authors):
        if year == None or len(authors) == 0:
            print "Warning: excluding publication due to missing information"
            print "    Publication type:", PublicationType[pub_type]
            print "    Title:", title
            print "    Year:", year
            print "    Authors:", ",".join(authors)
            return
        if title == None:
            print "Warning: adding publication with missing title [ %s %s (%s) ]" % (
            PublicationType[pub_type], year, ",".join(authors))
        idlist = []
        for a in authors:
            try:
                idlist.append(self.author_idx[a])
            except KeyError:
                a_id = len(self.authors)
                self.author_idx[a] = a_id
                idlist.append(a_id)
                self.authors.append(Author(a))
        self.publications.append(
            Publication(pub_type, title, year, idlist))
        if (len(self.publications) % 100000) == 0:
            print "Adding publication number %d (number of authors is %d)" % (len(self.publications), len(self.authors))

        if self.min_year == None or year < self.min_year:
            self.min_year = year
        if self.max_year == None or year > self.max_year:
            self.max_year = year

    def _get_collaborations(self, author_id, include_self):
        """
        Get the list of collaborations for particular author

        @type author_id: int
        @param author_id: the id of the author
        @type include_self: bool
        @param include_self: whether to include the collaboration with himself or not

        @rtype: dict
        @return: list of collaborations
        """
        data = {}
        for p in self.publications:
            if author_id in p.authors:
                for a in p.authors:
                    try:
                        data[a] += 1
                    except KeyError:
                        data[a] = 1
        if not include_self:
            del data[author_id]
        return data

    def get_coauthor_details(self, name):
        author_id = self.author_idx[name]
        data = self._get_collaborations(author_id, True)
        return [(self.authors[key].name, data[key])
                for key in data]

    def get_network_data(self):
        """
        Get all network data for all authors and their collaborations
        @rtype:    list
        @return:    list in the format of data[[name, amount_of_collaborations], set(all_collaborations)]
                    name = data[0][n][0],
                    amount_of_collaborations = data[0][n][1],
                    set_of_all_collaborations = data[1]
        """
        na = len(self.authors)

        nodes = [[self.authors[i].name, -1] for i in range(na)]
        links = set()
        for a in range(na):
            collab = self._get_collaborations(a, False)
            nodes[a][1] = len(collab)
            for a2 in collab:
                if a < a2:
                    links.add((a, a2))
        return (nodes, links)

    def get_author_by_name(self, name):
        data = []
        for p in self.publications:
            for i in p.authors:
                if str(name).lower() in str(self.authors[i].name).lower():
                    if self.authors[i].name not in data:
                        data.append(self.authors[i].name)
        return data

    def _build_authors_graph(self):
        """
        Build authors graph with each author name as nodes and the collaboration between them as edges.

        @author 1: CipherHat

        @rtype:   networkx.Graph()
        @return:  the Graph containing nodes and edges
        """
        all_data = self.get_network_data()
        # TODO refactor: revision on this part. whether to move the Graph code to its own class
        graph = Graph()
        # the nodes format will be {"id":int, "name":str}
        graph.add_nodes_from([(i, {"name": all_data[0][i][0]}) for i in range(len(all_data[0]))])
        graph.add_edges_from(all_data[1])
        return graph

    def get_degree_of_separation(self, author1, author2):
        """
        Get degree of separation between two specified authors. This method is using authors_graph that is generated
        during initialisation by executing _build_author_graphs method

        @author 1: CipherHat

        @type  author1: String
        @param author1: Name of the author. Example: "Author A"
        @type  author2: String
        @param author2: Name of the second author. Example: "Author B"

        @rtype:   String, int
        @return:  If there is any degree of separation between two authors, a number will be returned e.g: 1
                    If there is no degree of separation at all, String "X" will be returned.
                    If the two authors name are the same, String "No separation between the same authors" will be returned
                    If the author's name input is non existent, String "Not found" will be returned
        """
        if author1 == author2:
            return "No separation between the same authors"
        try:
            return shortest_path_length(self.authors_graph, self.author_idx[author1], self.author_idx[author2]) - 1
        except NetworkXNoPath:
            return "X"
        except NetworkXError as e:
            return "Not found"
        
    def get_degree_of_separation_visualisation(self, author1, author2):
        
        if author1 == author2:
            return "No separation between the same authors"
        
        # Compute all the shortest paths from author1 to author2
        try:
            list_of_paths = all_shortest_paths(self.authors_graph, self.author_idx[author1], self.author_idx[author2])
        except NetworkXError as e:
            return "Not found"
        
        g = Graph()
        # Add the shortest paths to the graph
        for path in list_of_paths:
            g.add_path(path)
        
        # Add attributes to nodes
        for i in g.nodes():
            g.node[i]['name']=self.authors[i].name
        
        return g

    def split_author_name(self, name):

        split_name = str(name).split(" ")
        split_len = len(split_name)

        data = []
        if split_len > 1:
            data = [name, split_name[split_len - 1], split_name[0], split_name[0] + " " + split_name[split_len - 1]]
        elif split_len == 1:
            data = [name, split_name[0], "", split_name[0]]
        return data

    def sort_author_by_name(self, name):
        """
        Get the sorted list of all authors with the specified keyword.

        @author 1: Ruvin, Sylvain
        @author 2: Dommy, CipherHat

        @type  name: String
        @param name: Name of the author or a keyword to be searched. Example: "Sam"

        @rtype:   dict
        @return:  A list containing the list of names of the author matching with the specified keyword
        """
        if len(str(name)) < 2:
            return []

        data = [self.split_author_name(author) for author in self.get_author_by_name(name)]

        # Lists for dividing before the sorting
        ln_exact = []
        ln_start = []
        ln_contain = []
        fn_exact = []
        fn_start = []
        fn_contain = []
        mn_all = []

        lower_name = str(name).lower()

        # Put every tuple in its correct list
        for a in data:
            low_ln = str(a[1]).lower()
            low_fn = str(a[2]).lower()
            if lower_name in low_ln:
                if low_ln == lower_name:
                    ln_exact.append(a)
                elif low_ln.startswith(lower_name):
                    ln_start.append(a)
                else:
                    ln_contain.append(a)
            elif lower_name in low_fn:
                if low_fn == lower_name:
                    fn_exact.append(a)
                elif low_fn.startswith(lower_name):
                    fn_start.append(a)
                else:
                    fn_contain.append(a)
            else:
                mn_all.append(a)

        # Sort every list
        ln_exact.sort(key=lambda tup: tup[3])
        ln_start.sort(key=lambda tup: tup[3])
        ln_contain.sort(key=lambda tup: tup[3])
        fn_exact.sort(key=lambda tup: tup[3])
        fn_start.sort(key=lambda tup: tup[3])
        fn_contain.sort(key=lambda tup: tup[3])
        mn_all.sort(key=lambda tup: tup[3])

        # Merge all sorted lists
        ln_exact.extend(ln_start)
        ln_exact.extend(fn_exact)
        ln_exact.extend(fn_start)
        ln_exact.extend(ln_contain)
        ln_exact.extend(fn_contain)
        ln_exact.extend(mn_all)

        return ln_exact


class DocumentHandler(handler.ContentHandler):
    TITLE_TAGS = ["sub", "sup", "i", "tt", "ref"]
    PUB_TYPE = {
        "inproceedings": Publication.CONFERENCE_PAPER,
        "article": Publication.JOURNAL,
        "book": Publication.BOOK,
        "incollection": Publication.BOOK_CHAPTER}

    def __init__(self, db):
        self.tag = None
        self.chrs = ""
        self.clearData()
        self.db = db

    def clearData(self):
        self.pub_type = None
        self.authors = []
        self.year = None
        self.title = None

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def startElement(self, name, attrs):
        if name in self.TITLE_TAGS:
            return
        if name in DocumentHandler.PUB_TYPE.keys():
            self.pub_type = DocumentHandler.PUB_TYPE[name]
        self.tag = name
        self.chrs = ""

    def endElement(self, name):
        if self.pub_type == None:
            return
        if name in self.TITLE_TAGS:
            return
        d = self.chrs.strip()
        if self.tag == "author":
            self.authors.append(d)
        elif self.tag == "title":
            self.title = d
        elif self.tag == "year":
            self.year = int(d)
        elif name in DocumentHandler.PUB_TYPE.keys():
            self.db.add_publication(
                self.pub_type,
                self.title,
                self.year,
                self.authors)
            self.clearData()
        self.tag = None
        self.chrs = ""

    def characters(self, chrs):
        if self.pub_type != None:
            self.chrs += chrs
