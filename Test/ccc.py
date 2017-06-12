import multiprocessing

def worker(num):
    """thread worker function"""
    print 'Worker:', num
    return

if __name__ == '__main__':
    jobs = []
    for i in range(4):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()
