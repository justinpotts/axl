import os
import random
import string
import sys

def generate(**keyword_parameters):
    path = ''
    if ('path' in keyword_parameters):
        path = keyword_parameters['path']
        print 'Path parameter found, ', keyword_parameters['path']
    else:
        path = sys.argv[1]

    if path is None or path.strip() == '' or path[len(path)-1] != '/':
        sys.exit('Error in path specification... Ensure path is not empty and ends with /')

    path += 'webext/'

    if not os.path.exists(path):
        os.makedirs(path)

    print 'Generating keys...'
    ext_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    print ext_key
    ext_name = 'axl' + ext_key
    print ext_name
    ext_id = 'axl' + ext_key + '@mozilla.org'
    print ext_id

    print 'Creating manifest...'
    manifest = open(path + 'manifest.json', 'w')
    print 'Manifest path: ' + path + 'manifest.json'
    manifest.write('{"manifest_version": 2, "name": "' + ext_name + '", "version": "1.0", "description": "Aides in efforts to improve automation testing in Firefox Add-ons.", "applications": { "gecko": { "id": "' + ext_id + '", "strict_min_version": "45.0" } }, "content_scripts": [ { "matches": ["*://justinpotts.github.io/project-axl-frontend/test?key=' + ext_name + '"], "js": ["genext.js"] } ] } ')
    manifest.close()
    print 'Manifest created'

    print 'Creating JS...'
    genextjs = open(path + 'genext.js', 'w')
    print 'JS path: ' + path + 'genext.js'
    genextjs.write('document.getElementById(\'indicator\').innerHTML = \'<p><img id="success" src="media/img/check-mark.jpg"></p><p><span class="download-completion">It works!</span></p><p><span class="install-instructions">To disable or remove the add-on, visit about:addons.</span></p>\';')
    genextjs.close()
    print 'JS created'

    os.chdir(path)
    print 'Packaging extension...'
    os.system('zip -r ../' + ext_name + '.xpi *')
    print 'Extension packaged in .xpi at ' + path + ext_name + '.xpi'
    os.chdir('../')
    print 'Cleaning up...'

    os.chdir('webext/')
    os.system('rm manifest.json')
    os.system('rm genext.js')
    os.chdir('..')
    os.system('rm -rf webext/')

    print 'Success! Web extension at ' + path + ext_name + '.xpi'

    return ext_name + '.xpi'

if __name__ == '__main__':
    generate()
