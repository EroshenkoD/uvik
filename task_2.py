import json
import click
import datetime


@click.command()
@click.option('--add', '-a', help='You can add new tasks', multiple=True)
@click.option('--delete', '-d', help="You can delete open tasks by specifying the task's ID", multiple=True, type=int)
@click.option('--view', '-v', is_flag=True, help='You can view open tasks')
@click.option('--complete', '-c', type=int, help="You can mark a task as completed by specifying the task's ID")
@click.option('--statistic', '-s', is_flag=True, help="You can see the statistics of completed tasks")
def main(add, delete, view, complete, statistic):
    try:
        data = json.load(open('to_do.json'))
    except:
        data = []
    if add:
        add_task(data, add)
    if view:
        view_open_task(data)
    if delete:
        delete_task(data, delete)
    if complete:
        complete_task(data, complete)
    if statistic:
        statistic_complete_task(data)


def list_open_task(data):
    return [i for i in data if i['status'] == '0']


def write_json(data):
    with open('to_do.json', 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def new_id(data):
    return max([i['id'] for i in data]) + 1


def delete_task(data, delete_data):
    for id_task_for_del in delete_data:
        counter = 0
        text_answer = ''
        for task in data:
            if task['id'] == id_task_for_del:
                for task_open in list_open_task(data):
                    if task_open['id'] == id_task_for_del:
                        del data[counter]
                        text_answer = f"Task with ID {task['id']} have deleted"
                if not text_answer:
                    text_answer = f"Task with ID {task['id']} closed"
            counter += 1
        if not text_answer:
            text_answer = f"Task with ID {id_task_for_del} don't find"
        click.echo(text_answer)
    write_json(data)


def add_task(data, add_data):
    for task in add_data:
        if data:
            id_task = new_id(data)
        else:
            id_task = 1
        temp = {
            'id': id_task,
            'task': task,
            'status': '0'
        }
        data.append(temp)
    write_json(data)
    click.echo("Tasks were added to the list")


def view_open_task(data):
    for i in list_open_task(data):
        click.echo(f"Task's ID {i['id']} - {i['task']}")


def complete_task(data, complete_id_task):
    text_answer = ''
    for task in data:
        if task['id'] == complete_id_task:
            if task['status'] == '0':
                task['status'] = datetime.date.today().strftime("%Y.%m.%d")
                text_answer = f"Task with ID {task['id']} was marked as a performed"
            else:
                text_answer = f"Task with ID {task['id']} was completed in {task['status']}"
    if not text_answer:
        text_answer = f"Task with ID {complete_id_task} not found"
    click.echo(text_answer)
    write_json(data)


def statistic_complete_task(data):
    if not data:
        click.echo("You have no completed tasks")
    else:
        dict_statistic = {}
        for task in data:
            if task['status'] != "0":
                if task['status'] in dict_statistic:
                    dict_statistic[task['status']] += 1
                else:
                    dict_statistic[task['status']] = 1
    if not dict_statistic:
        click.echo("You have no completed tasks")
    else:
        for key, value in dict_statistic.items():
            click.echo(f"{key}: you've completed {value} tasks!")


if __name__ == '__main__':
    main()
