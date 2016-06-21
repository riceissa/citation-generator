# Citation generator for Wikipedia

Sample usage:

```bash
$ ./cite.sh 'http://www.nytimes.com/2014/04/26/your-money/giving-away-money-and-making-sure-its-put-to-work.html'
<ref>{{cite web |url=http://www.nytimes.com/2014/04/26/your-money/giving-away-money-and-making-sure-its-put-to-work.html |date=April 25, 2014 |title=Donating, and Making Sure the Money Is Put to Work |publisher=The New York Times |accessdate=June 18, 2016}}</ref>
```

Inspired by [RefScript](https://en.wikipedia.org/wiki/User:Ark25/RefScript).

# TODO

Here I'll keep a list of things I need to improve, which will mostly be a list of websites for which the script doesn't work very well.

- Fix `cite.sh` so it doesn't depend on the directory where you call it from/where `cite.py` is stored.
- Doesn't work very well on <http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2205967/>.
