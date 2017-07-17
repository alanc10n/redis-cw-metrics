import argparse
import boto3
import json
from redis import StrictRedis

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', default='localhost', help='Host')
    parser.add_argument('-p', '--port', default=6379, type=int, help='Port')
    parser.add_argument('-d', '--dimension', 
                        action='append',
                        help='Dimension JSON to specify custom dimensions, e.g. {"Name": "Server", "Value": "web1"}')

    args = parser.parse_args()
    return args

def get_redis_info(args):
    redis = StrictRedis(host=args.host, port=args.port)
    info = redis.info()
    print(info)
    return info

def get_metric_data(key, dimensions, value):
    metric_data = { 'MetricName': key,
                    'Dimensions': dimensions,
                    'Value': value
                  }
    return [metric_data,]

def get_metrics_of_interest(redis_info):
    metrics = {
                'UsedMemory': redis_info['used_memory'],
                'Keyspace': redis_info['db0']['keys'],
                'EvictedKeys': redis_info['evicted_keys'],
                'UsedMemoryPeak': redis_info['used_memory_peak']
              }

    return metrics

def publish_redis_info(args, redis_info):
    dimensions = [json.loads(d) for d in args.dimension]
    cw = boto3.client('cloudwatch')
    metrics_of_interest = get_metrics_of_interest(redis_info)

    for k,v in metrics_of_interest.items():
        metric_data = get_metric_data(k, dimensions, v)
        print(metric_data)
        cw.put_metric_data(Namespace='Redis',
                           MetricData=metric_data)


def main():
    args = parse_args()
    redis_info = get_redis_info(args)
    publish_redis_info(args, redis_info)

if __name__ == '__main__':
    main()
