import concurrent.futures
import os
import logging
from queue import Queue
from threading import Lock

class ThreadPoolManager:
    def __init__(self, max_workers=None):
        """
        初始化线程池
        :param max_workers: 最大工作线程数，默认使用SLURM分配的CPU核心数
        """
        # 自动获取Slurm分配的CPU核心数
        self.max_workers = max_workers or int(os.getenv('SLURM_CPUS_PER_TASK', os.cpu_count() or 4))
        
        # 创建线程池
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers,
            thread_name_prefix="ImgWorker"
        )
        
        # 任务队列和锁
        self.task_queue = Queue()
        self.result_lock = Lock()
        self.results = []
        self.completed_count = 0
        self.total_tasks = 0
        
        
    def submit_task(self, func, *args, **kwargs):
        """提交单个任务到线程池"""
        self.total_tasks += 1
        future = self.executor.submit(func, *args, **kwargs)
        future.add_done_callback(self._task_completed)
        return future
    
    def submit_batch(self, func, arg_list):
        """批量提交任务"""
        self.total_tasks += len(arg_list)
        futures = []
        for args in arg_list:
            if isinstance(args, tuple):
                future = self.executor.submit(func, *args)
            else:
                future = self.executor.submit(func, args)
            future.add_done_callback(self._task_completed)
            futures.append(future)
        return futures
    
    def _task_completed(self, future):
        """任务完成回调函数"""
        try:
            result = future.result()
            with self.result_lock:
                self.results.append(result)
                self.completed_count += 1
                
                # 进度报告
                if self.completed_count % max(1, self.total_tasks // 10) == 0:
                    progress = self.completed_count / self.total_tasks * 100
                    print(f"处理进度: {progress:.1f}% ({self.completed_count}/{self.total_tasks})")
        except Exception as e:
            self.logger.error(f"任务执行失败: {str(e)}")
    
    def wait_completion(self):
        """等待所有任务完成"""
        self.executor.shutdown(wait=True)
        print(f"所有任务完成! 成功: {len(self.results)}/{self.total_tasks}")
        return self.results
    
    def get_progress(self):
        """获取当前进度"""
        with self.result_lock:
            return self.completed_count, self.total_tasks
gthread_pool = ThreadPoolManager()