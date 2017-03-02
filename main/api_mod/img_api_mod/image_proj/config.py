#For reading image from s3 and setting in pipeline
kafkaAPIConfig = {
                'topic_ip': 'image_reader',
                'topic_op': 'image_process_generator'
}

kafkaRealTimeImageReadOutput = {
	'topic_ip': 'image_reader',
	'topic_op': 'real_time_image_process_generator'
}


kafkaRealTimeImageReadOutput = {
    'topic_ip': 'real_time_image_process_generator',
    'topic_op': 'get_image_from_storage'
}


#For image input in processengine
kafkaImageReadOutput = {
    'topic_ip': 'image_process_generator',
    'topic_op': 'get_image_from_storage'
}

kafkaImageGetS3Output = {
	'topic_ip': 'get_image_from_storage',
	'topic_op': 'image_processor'
}

kafkaImageProcessOutput = {
    'topic_ip': 'image_processor',
    'topic_op': 'image_process_output'
}


