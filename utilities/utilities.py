import progressbar

class Sort():
    # merge sort
    def __init__(self, arrays):
        if len(arrays) == 0:
            print('No data to sorted ..')
            self.__sorted_arrays = []
            self.__grouped_arrays = dict()
            return

        self.__bar = progressbar.ProgressBar(max_value=len(arrays) * 2, widgets=[
            'sorting %d data ' % (len(arrays)),
            progressbar.Bar(),
            ' (', progressbar.ETA(), ') ',
        ])

        self.__counter = 0
        self.__bar.start()
        self.__sorted_arrays = self.__sort__(arrays)
        self.__bar.finish(end='\n')

        self.__bar = progressbar.ProgressBar(max_value=len(arrays) * 2, widgets=[
            'grouping %d data ' % (len(arrays)),
            progressbar.Bar(),
            ' (', progressbar.ETA(), ') ',
        ])

        self.__bar.start()
        self.__grouped_arrays = self.__group__(self.__sorted_arrays)
        self.__bar.finish(end='\n\n')

    def __sort__(self, arrays):
        # doing merge sort
        self.__counter += 1
        self.__bar.update(self.__counter)

        length = len(arrays)
        if length < 2:
            return arrays

        middle = length//2

        left = arrays[:middle]
        right = arrays[middle:]
        
        left = self.__sort__(left)
        right = self.__sort__(right)
        
        return self.__combine__(left, right)

    def __combine__(self, left, right):
        if not len(left) or not len(right):
            return left or right

        arrays = []
        i, j = 0, 0
        while len(arrays) < len(left) + len(right):
            if left[i] < right[j]:
                arrays.append(left[i])
                i+=1
            else:
                arrays.append(right[j])
                j+=1
            
            if i == len(left) or j == len(right):
                arrays.extend(left[i:] or right[j:])
                break

        return arrays

    def __group__(self, arrays):
        group = []
        prev_item = None
        counter = 0
        self.__counter = counter

        for item in arrays:
            self.__counter += 1
            self.__bar.update(self.__counter)

            counter += 1
            if item != prev_item:
                counter = 1
                group.append((item, counter))
            else:
                group[-1] = (item, counter)
            prev_item = item

        return tuple(group)

    def get(self):
        return self.__sorted_arrays

    def count(self, group=True):
        if group:
            return self.__grouped_arrays

        return len(self.__sorted_arrays)


