import sys
import json
from urllib.parse import urlparse, parse_qs

class HierarchicalAPI:
    def __init__(self):
        self.orgs = {}
        self.org_counter = 1
        self.team_counter = 1
        self.member_counter = 1
    
    def handle_request(self, method, path, data=None):
        parts = [p for p in path.split('/') if p]
        
        if not parts or parts[0] != 'orgs':
            return {'error': 'Invalid path'}, 404
        
        if len(parts) == 1:  # /orgs
            return self.handle_orgs(method, data)
        elif len(parts) == 2:  # /orgs/:orgId
            org_id = parts[1]
            return self.handle_org(method, org_id, data)
        elif len(parts) == 3:  # /orgs/:orgId/teams
            org_id = parts[1]
            if parts[2] != 'teams':
                return {'error': 'Invalid path'}, 404
            return self.handle_teams(method, org_id, data)
        elif len(parts) == 4:  # /orgs/:orgId/teams/:teamId
            org_id = parts[1]
            team_id = parts[3]
            if parts[2] != 'teams':
                return {'error': 'Invalid path'}, 404
            return self.handle_team(method, org_id, team_id, data)
        elif len(parts) == 5:  # /orgs/:orgId/teams/:teamId/members
            org_id = parts[1]
            team_id = parts[3]
            if parts[2] != 'teams' or parts[4] != 'members':
                return {'error': 'Invalid path'}, 404
            return self.handle_members(method, org_id, team_id, data)
        elif len(parts) == 6:  # /orgs/:orgId/teams/:teamId/members/:memberId
            org_id = parts[1]
            team_id = parts[3]
            member_id = parts[5]
            if parts[2] != 'teams' or parts[4] != 'members':
                return {'error': 'Invalid path'}, 404
            return self.handle_member(method, org_id, team_id, member_id, data)
        else:
            return {'error': 'Invalid path'}, 404
    
    def handle_orgs(self, method, data):
        if method == 'GET':
            return list(self.orgs.values()), 200
        elif method == 'POST':
            org_id = str(self.org_counter)
            self.org_counter += 1
            org = {
                'id': org_id,
                'name': data.get('name', ''),
                'teams_url': f'/orgs/{org_id}/teams'
            }
            self.orgs[org_id] = org
            return org, 201
        return {'error': 'Method not allowed'}, 405
    
    def handle_org(self, method, org_id, data):
        if org_id not in self.orgs:
            return {'error': 'Organization not found'}, 404
        
        if method == 'GET':
            return self.orgs[org_id], 200
        elif method == 'PUT':
            self.orgs[org_id].update(data)
            return self.orgs[org_id], 200
        elif method == 'DELETE':
            del self.orgs[org_id]
            return {'message': 'Deleted'}, 200
        return {'error': 'Method not allowed'}, 405
    
    def handle_teams(self, method, org_id, data):
        if org_id not in self.orgs:
            return {'error': 'Organization not found'}, 404
        
        if 'teams' not in self.orgs[org_id]:
            self.orgs[org_id]['teams'] = {}
        
        if method == 'GET':
            return list(self.orgs[org_id]['teams'].values()), 200
        elif method == 'POST':
            team_id = str(self.team_counter)
            self.team_counter += 1
            team = {
                'id': team_id,
                'name': data.get('name', ''),
                'org_id': org_id,
                'members_url': f'/orgs/{org_id}/teams/{team_id}/members'
            }
            self.orgs[org_id]['teams'][team_id] = team
            return team, 201
        return {'error': 'Method not allowed'}, 405
    
    def handle_team(self, method, org_id, team_id, data):
        if org_id not in self.orgs:
            return {'error': 'Organization not found'}, 404
        if 'teams' not in self.orgs[org_id] or team_id not in self.orgs[org_id]['teams']:
            return {'error': 'Team not found'}, 404
        
        team = self.orgs[org_id]['teams'][team_id]
        
        if method == 'GET':
            return team, 200
        elif method == 'PUT':
            team.update(data)
            return team, 200
        elif method == 'DELETE':
            del self.orgs[org_id]['teams'][team_id]
            return {'message': 'Deleted'}, 200
        return {'error': 'Method not allowed'}, 405
    
    def handle_members(self, method, org_id, team_id, data):
        if org_id not in self.orgs:
            return {'error': 'Organization not found'}, 404
        if 'teams' not in self.orgs[org_id] or team_id not in self.orgs[org_id]['teams']:
            return {'error': 'Team not found'}, 404
        
        team = self.orgs[org_id]['teams'][team_id]
        if 'members' not in team:
            team['members'] = {}
        
        if method == 'GET':
            return list(team['members'].values()), 200
        elif method == 'POST':
            member_id = str(self.member_counter)
            self.member_counter += 1
            member = {
                'id': member_id,
                'name': data.get('name', ''),
                'team_id': team_id,
                'org_id': org_id
            }
            team['members'][member_id] = member
            return member, 201
        return {'error': 'Method not allowed'}, 405
    
    def handle_member(self, method, org_id, team_id, member_id, data):
        if org_id not in self.orgs:
            return {'error': 'Organization not found'}, 404
        if 'teams' not in self.orgs[org_id] or team_id not in self.orgs[org_id]['teams']:
            return {'error': 'Team not found'}, 404
        
        team = self.orgs[org_id]['teams'][team_id]
        if 'members' not in team or member_id not in team['members']:
            return {'error': 'Member not found'}, 404
        
        member = team['members'][member_id]
        
        if method == 'GET':
            return member, 200
        elif method == 'PUT':
            member.update(data)
            return member, 200
        elif method == 'DELETE':
            del team['members'][member_id]
            return {'message': 'Deleted'}, 200
        return {'error': 'Method not allowed'}, 405

def main():
    port = input().strip()
    print(f"Listening on :{port}")

if __name__ == "__main__":
    main()