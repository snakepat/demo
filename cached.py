#!/usr/bin/python3
# -*- coding: utf-8 -*- #考虑到python3默认的编译格式本来就是utf-8,这条多余了

from ctypes import FormatError
import hashlib
import io
import json
import logging
import os
import time
# import sys
# import unicodedata


#配置日志
logging.basicConfig(
    filename='cache.log',  # 日志文件路径
    level=logging.INFO,  # 设置日志级别为INFO
    format='%(asctime)s %(levelname)s %(message)s',  # 日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
)

class cached(object):
    usecache = True
    verbose = False #是否输出调试信息
    # debug = False
    hashcachepath = os.path.join(os.getcwd(),"aches.json")
    cache = {}
    cacheloaded = False
    dirty = False
    semaphore = None

    def __init__(self, f):
        self.f = f
        super(cached, self).__init__()


    def __call__(self, *args):
        assert len(args) > 0
        # result = None
        path = args[0]
        dir, file = os.path.split(path) # the 'filepath' parameter
        absdir = os.path.abspath(dir) # 取绝对路径
        #如果已经存储了该文件的缓存
        if absdir in cached.cache:
            entry = cached.cache[absdir]
            if file in entry:
                info = entry[file]
                if self.f.__name__ in info \
                    and info['size'] == os.path.getsize(path) \
                    and info['mtime'] == int(os.path.getmtime(path)) \
                    and self.f.__name__ in info \
                    and cached.usecache:
                    result = info[self.f.__name__]
                    # if cached.debug:
                    # 	pdbg("Cache hit for file '{}',\n{}: {}\nsize: {}\nmtime: {}".format(
                    # 		path, self.f.__name__,
                    # 		result,
                    # 		info['size'], info['mtime']))
                else:
                    result = self.f(*args)
                    self._store(info, path, result)
            else:
                result = self.f(*args)
                entry[file] = {}
                info = entry[file]
                self._store(info, path, result)
        else:
            #如果之前没有缓存，就存缓存
            result = self.f(*args)
            cached.cache[absdir] = {}
            entry = cached.cache[absdir]
            entry[file] = {}
            info = entry[file]
            self._store(info, path, result)


        return result
        
    def _store(self, info, path, value):
        cached.dirty = True
        info['size'] = os.path.getsize(path)
        info['mtime'] = int(os.path.getmtime(path))
        info[self.f.__name__] = value
        # if cached.debug:
        # 	situation = "Storing cache"
        # 	if cached.usecache:
        # 		situation = "Cache miss"
        # 	pdbg((situation + " for file '{}',\n{}: {}\nsize: {}\nmtime: {}").format(
        # 		path, self.f.__name__,
        # 		value,
        # 		info['size'], info['mtime']))

        # periodically save to prevent loss in case of system crash
        # now = time.time()
        # if now - gvar.last_cache_save >= const.CacheSavePeriodInSec:
        #     # if cached.debug:
        #     #     pdbg("Periodically saving Hash Cash")
        #     cached.savecache()
        #     gvar.last_cache_save = now
    

    def get_cache(self):
        return self.cache
    

    @staticmethod
    def save_cahe():
        jsondump(cached.cache, cached.hashcachepath, cached.semaphore)
        return
    
    #输入是当前文件运行存在的缓存
    @staticmethod
    def load_cahe(existingcache = {}):
    # def loadcache():
    # load cache even we don't use cached hash values,
    # because we will save (possibly updated) and hash values
        if not cached.cacheloaded: # no double-loading
            if cached.verbose:
                print("Loading Hash Cache File '{}'...".format(cached.hashcachepath))
            if os.path.exists(cached.hashcachepath):
                try:
                    cached.cache = jsonload(cached.hashcachepath)
                    # pay the history debt ...
                    # TODO: Remove some time later when no-body uses the old bin format cache
                    # if cached.isbincache(cached.cache):
                    #     pinfo("ONE TIME conversion for binary format Hash Cache ...")
                    #     stringifypickle(cached.cache)
                    #     pinfo("ONE TIME conversion finished")
                    ##################################################
                    ##需要考虑新老缓存的结合
                    # if existingcache: # not empty
                    #     if cached.verbose:
                    #         print("Merging with existing Hash Cache")
                    #     cached.mergeinto(existingcache, cached.cache)
                    cached.cacheloaded = True
                    if cached.verbose:
                        print("Hash Cache File loaded.")
                #except (EOFError, TypeError, ValueError, UnicodeDecodeError) as ex:
                except Exception as ex:
                    logging.error("Fail to load the Hash Cache, no caching.\n{}".format(FormatError(ex)))
                    cached.cache = existingcache
            else:
                if cached.verbose:
                    print("Hash Cache File '{}' not found, no caching".format(cached.hashcachepath))
        else:
            if cached.verbose:
                print("Not loading Hash Cache since 'cacheloaded' is '{}'".format(cached.cacheloaded))

        return cached.cacheloaded
    
    #cleancache方法用于清理缓存中的无效条目，并保存可能被修改的缓存，以保持缓存的有效性。
    # @staticmethod
    # def cleancache():
    #     if cached.loadcache():
    #         for absdir in cached.cache.keys():
    #             if not os.path.exists(absdir):
    #                 if cached.verbose:
    #                     print("Directory: '{}' no longer exists, removing the cache entries".format(absdir))
    #                 cached.dirty = True
    #                 del cached.cache[absdir]
    #             else:
    #                 oldfiles = cached.cache[absdir]
    #                 files = {}
    #                 needclean = False
    #                 for f in oldfiles.keys():
    #                     #p = os.path.join(absdir, f)
    #                     p = os.path.join(absdir, f)
    #                     if os.path.exists(p):
    #                         files[f] = oldfiles[f]
    #                     else:
    #                         if cached.verbose:
    #                             needclean = True
    #                             print("File '{}' no longer exists, removing the cache entry".format(p))

    #                 if needclean:
    #                     cached.dirty = True
    #                     cached.cache[absdir] = files
    #     cached.savecache()


@cached
def md5(buf):
    m = hashlib.md5()
    # with io.open(filepath, 'rb') as f:
    #     # while True:
    #     #     buf = f.read(slice_size)
    if buf:
        m.update(buf) #使用 m.update(buf) 方法将数据块 buf 更新到这个哈希对象中。这样做的目的是逐步构建整个文件的哈希值。
    else:
        logging.error("md5 caculate error happen")
    return m.hexdigest()

# slice md5 for baidu rapidupload
# @cached
# def slice_md5(filename):
# 	m = hashlib.md5()
# 	with io.open(filename, 'rb') as f:
# 		buf = f.read(256 * 1024)
# 		m.update(buf)

# 	return m.hexdigest()

#将数据保存为json
def jsondump(data, filename, semaphore):
    if semaphore:
        with semaphore:
            with io.open(filename, 'w', encoding = 'utf-8') as f:
                jsondump_actual(data, f)
    else:
        with io.open(filename, 'w', encoding = 'utf-8') as f:
            jsondump_actual(data, f)

def jsonload(filename):
	with io.open(filename, 'r', encoding = 'utf-8') as f:
		return json.load(f)

def jsondump_actual(data, f):
	# if sys.version_info[0] == 2:
	# 	f.write(unicodedata(json.dumps(data, ensure_ascii = False, sort_keys = True, indent = 2)))
	# elif sys.version_info[0] == 3:
	json.dump(data, f, ensure_ascii = False, sort_keys = True, indent = 2)
