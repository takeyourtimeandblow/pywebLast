from flask import Blueprint, jsonify, request
from db_session import create_session
from models.jobs import Jobs

jobs_api = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)

@jobs_api.route('/api/jobs', methods=['GET'])
def get_jobs():
    session = create_session()
    jobs = session.query(Jobs).all()

    return jsonify({
        'jobs': [
            {
                'id': job.id,
                'team_leader': job.team_leader,
                'job': job.job,
                'work_size': job.work_size,
                'collaborators': job.collaborators,
                'is_finished': job.is_finished
            } for job in jobs
        ]
    })

@jobs_api.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    session = create_session()
    job = session.get(Jobs, job_id)

    if not job:
        return jsonify({'error': 'Not found'}), 404

    return jsonify({
        'job': {
            'id': job.id,
            'team_leader': job.team_leader,
            'job': job.job,
            'work_size': job.work_size,
            'collaborators': job.collaborators,
            'is_finished': job.is_finished
        }
    })

@jobs_api.route('/api/jobs', methods=['POST'])
def add_job():
    session = create_session()

    if not request.json:
        return jsonify({'error': 'Empty request'}), 400

    job_id = request.json.get('id')
    if job_id and session.get(Jobs, job_id):
        return jsonify({'error': 'Id already exists'}), 400

    job = Jobs(
        id=job_id,
        team_leader=request.json.get('team_leader'),
        job=request.json.get('job'),
        work_size=request.json.get('work_size'),
        collaborators=request.json.get('collaborators'),
        is_finished=request.json.get('is_finished', False)
    )

    session.add(job)
    session.commit()

    return jsonify({'success': 'OK'})

@jobs_api.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    session = create_session()
    job = session.get(Jobs, job_id)

    if not job:
        return jsonify({'error': 'Not found'}), 404

    session.delete(job)
    session.commit()

    return jsonify({'success': 'OK'})

@jobs_api.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    session = create_session()
    job = session.get(Jobs, job_id)

    if not job:
        return jsonify({'error': 'Not found'}), 404

    if not request.json:
        return jsonify({'error': 'Empty request'}), 400

    job.team_leader = request.json.get('team_leader', job.team_leader)
    job.job = request.json.get('job', job.job)
    job.work_size = request.json.get('work_size', job.work_size)
    job.collaborators = request.json.get('collaborators', job.collaborators)
    job.is_finished = request.json.get('is_finished', job.is_finished)

    session.commit()

    return jsonify({'success': 'OK'})
