# coding=utf-8
'''ID 生成模块'''

from ext import cache


def next_user_id():
    '''获取下一个可用用户ID'''
    key = 'user:id:next'
    return cache.incr(key)


def next_song_id():
    '''获取下一个可用歌曲ID'''
    key = 'song:id:next'
    return cache.incr(key)


def next_audio_id():
    '''获取下一个可用音频ID'''
    key = 'audio:id:next'
    return cache.incr(key)


def next_comment_id():
    '''获取下一个可用评论ID'''
    key = 'comment:id:next'
    return cache.incr(key)
