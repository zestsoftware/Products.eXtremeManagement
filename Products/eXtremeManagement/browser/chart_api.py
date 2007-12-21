BASE_URL = 'http://chart.apis.google.com/chart?'

LINE = 0
LINES = 1
HBAR = 2
VBAR = 3
HBARGROUP = 4
VBARGROUP = 5
PIE = 6
PIE3D = 7
VENN = 8
SCATTER = 9

CHART_TYPES = ['lc', 'lxy', 'bhs', 'bvs', 'bhg', 'bvg', 'p', 'p3', 'v', 's']


class Chart(object):

    def __init__(self, type, data, size):
        self.setType(type)
        self.setData(data)
        self.setSize(size)
        self._labelx = None
        self._labelxy = None
        self._datacolors = None
        self._legend = None
        self._custom = None

    def setType(self, type):
        """Generates the string needed to set the chart Type in the google
           chart api. Only a few values are allowed.

           We start with a few correct calls:

           >>> g = Chart(0, [1], (0,0))
           >>> g._type
           'lc'
           >>> g.setType(HBAR)
           >>> g._type
           'bhs'
           >>> g.setType(PIE3D)
           >>> g._type
           'p3'
           >>> g.setType(VENN)
           >>> g._type
           'v'

           Let's try some unsupported types:

           >>> RADAR = 'radar'
           >>> g.setType(RADAR)
           >>> g._type
           'lc'
           >>> MAP = len(CHART_TYPES)
           >>> g.setType(MAP)
           >>> g._type
           'lc'
           >>> RING = -1
           >>> g.setType(RING)
           >>> g._type
           'lc'
        """
        if type < len(CHART_TYPES) and type >= 0:
            self._type = CHART_TYPES[type]
        else:
            self._type = CHART_TYPES[0]

    def setData(self, data):
        if isinstance(data[0], list) or isinstance(data[0], tuple):
            all_data = []
            maxValue = 0
            for dataset in data:
                localmax = max(dataset)
                if self._type.startswith('b'):
                    maxValue += localmax
                else:
                    maxValue = max([maxValue, localmax])
            maxValue = max(maxValue, 1)
            for dataset in data:
                all_data.append(self._encodeData(dataset, maxValue))
            self._data = ','.join(all_data)
        else:
            maxValue = max(data)
            maxValue = max(maxValue, 1)
            self._data = self._encodeData(data, maxValue)

    def _encodeData(self, data, maxValue):
        """Provides the simple Encoding for google charts.

           >>> g = Chart(0, [1], (0,0))
           >>> g._encodeData([1], 1)
           '9'
           >>> g._encodeData([0,1], 1)
           'A9'
           >>> g._encodeData([0,1,2,3,4,5,6,7,8,9,10], 10)
           'AGMSYekqw29'
           >>> g._encodeData([0,1,2,3,4,None,6,7,8,9,10], 10)
           'AGMSY_kqw29'

           and one example from the google help page:

           >>> g._encodeData([0,19,27,53,61], 61)
           'ATb19'
        """
        simpleEncoding = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        simpleEncoding += 'abcdefghijklmnopqrstuvwxyz'
        simpleEncoding += '0123456789'

        encodedData = ''
        for i in data:
            try:
                if i>=0:
                    index = (len(simpleEncoding)-1)*i / maxValue
                    encodedData += simpleEncoding[index]
                else:
                    encodedData += '_'
            except TypeError:
                encodedData += '_'
        return encodedData

    def setSize(self, size):
        """Set the size for this chart, but adhere to the google rules:
           1) No more than 300,000 pixels
           2) Height or width has 1000 pixels maximum
           3) Height or width has 10 pixels minimum

           First lets try some normal calls:

           >>> g1 = Chart(0,[1],(300,200))
           >>> g1._size
           (300, 200)
           >>> g2 = Chart(0,[1],(1000,300))
           >>> g2._size
           (1000, 300)
           >>> g3 = Chart(0,[1],(300,1000))
           >>> g3._size
           (300, 1000)
           >>> g4 = Chart(0,[1],(600,500))
           >>> g4._size
           (600, 500)
           >>> g5 = Chart(0,[1],(500,600))
           >>> g5._size
           (500, 600)
           >>> g6 = Chart(0,[1],(800,375))
           >>> g6._size
           (800, 375)
           >>> g7 = Chart(0,[1],(375,800))
           >>> g7._size
           (375, 800)

           Next, try some calls that need resizing:

           >>> g8 = Chart(0,[1],(1000,1000))
           >>> g8._size
           (547, 547)
           >>> g9 = Chart(0,[1],(2000,100))
           >>> g9._size
           (1000, 50)
           >>> g10 = Chart(0,[1],(100,2000))
           >>> g10._size
           (50, 1000)
           >>> g11 = Chart(0,[1],(5,5))
           >>> g11._size
           (10, 10)
           >>> g12 = Chart(0,[1],(2000,10))
           >>> g12._size
           (1000, 10)
           >>> g13 = Chart(0,[1],(0,0))
           >>> g13._size
           (10, 10)
        """
        width = size[0]
        height = size[1]
        if width*height > 300000:
            factor = (300000.0 / (width*height))**0.5
            width = int(factor * width)
            height = int(factor * height)
        if width > 1000:
            factor = 1000.0 / width
            width = int(factor * width)
            height = int(factor * height)
        if height > 1000:
            factor = 1000.0 / height
            width = int(factor * width)
            height = int(factor * height)
        width = max(width, 10)
        height = max(height, 10)
        self._size = (width, height)

    def setLabels(self, labels):
        """Generates the labels for the google chart api

           >>> g = Chart(LINE, [1], (0,0))
           >>> g._labelx == None
           True
           >>> g._labelxy == None
           True
           >>> g.setLabels(([1], ['a']))
           >>> g._labelxy
           '0:|1|1:|a'
           >>> g._labelx == None
           True
           >>> g.setLabels(([1,2,3,4],['a', 'b', 3, 'd']))
           >>> g._labelx == None
           True
           >>> g._labelxy
           '0:|1|2|3|4|1:|a|b|3|d'
           >>> g.setType(PIE)
           >>> g.setLabels(['open', 'close'])
           >>> g._labelx
           'open|close'
           >>> g._labelxy == None
           True
        """
        if self._type == 'p' or self._type == 'p3':
            self._labelx = '|'.join([str(i) for i in labels])
            self._labelxy = None
        else:
            xlab = '|'.join([str(i) for i in labels[0]])
            ylab = '|'.join([str(i) for i in labels[1]])
            self._labelx = None
            self._labelxy = '0:|%s|1:|%s' % (xlab, ylab)

    def setDataColors(self, colors):
        self._datacolors = ','.join([str(i) for i in colors])

    def setLegend(self, legend):
        self._legend = '|'.join([str(i) for i in legend])

    def setCustom(self, custom):
        self._custom = custom

    def getUrl(self):
        url = BASE_URL
        url += 'chs=%dx%d' % (self._size[0], self._size[1])
        url += '&chd=s:%s' % (self._data)
        url += '&cht=%s' % (self._type)
        if self._labelx:
            url += '&chl=%s' % self._labelx
        if self._labelxy:
            url += '&chxt=x,y&chxl=%s' % self._labelxy
        if self._datacolors:
            url += '&chco=%s' % self._datacolors
        if self._legend:
            url += '&chdl=%s' % self._legend
        if self._custom:
            url += self._custom
        return url


def nice_axis_step(number):
    """Returns a nice step size if the maximum number is <number>
       This is handy when you want a maximum of 10 axis labels, but
       the maximum of your data is not fixed.

       >>> nice_axis_step(0)
       1
       >>> nice_axis_step(1)
       1
       >>> nice_axis_step(2)
       1
       >>> nice_axis_step(10)
       2
       >>> nice_axis_step(11)
       2
       >>> nice_axis_step(40)
       5
       >>> nice_axis_step(95)
       10
       >>> nice_axis_step(105)
       20
       >>> nice_axis_step(100000000)
       20000000
    """
    nice_steps = nice_step_generator()
    step = nice_steps.next()
    while(1):
        if number/step < 10:
            return step
        step = nice_steps.next()


def nice_step_generator():
    """Generator for the list [1, 2, 5, 10, 20, 50, 100,....]
       This is a helper function for the nice_axis_step

       >>> gen = nice_step_generator()

       >>> gen.next()
       1
       >>> gen.next()
       2
       >>> gen.next()
       5
       >>> gen.next()
       10
       >>> gen.next()
       20
       >>> gen.next()
       50
       >>> gen.next()
       100
    """
    order = 1
    while(1):
        yield order*1
        yield order*2
        yield order*5
        order *= 10


if __name__ == '__main__':
    import doctest
    doctest.testmod()
