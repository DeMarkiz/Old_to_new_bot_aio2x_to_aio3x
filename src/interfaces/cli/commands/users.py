import asyncio
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from ....application.use_cases.user_management import UserManagementUseCase
from ....domain.entities.user import User
from ..main import get_user_management

app = typer.Typer(help="Управление пользователями")
console = Console()


def format_user(user: User) -> dict:
    """Форматирование данных пользователя для вывода."""
    return {
        "ID": user.id,
        "Telegram ID": user.telegram_id,
        "Username": user.username or "-",
        "First Name": user.first_name or "-",
        "Last Name": user.last_name or "-",
        "Active": "Yes" if user.is_active else "No",
        "Admin": "Yes" if user.is_admin else "No",
        "Created": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "Updated": user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
    }


@app.command("list")
def list_users(active_only: bool = typer.Option(False, "--active", "-a", help="Показать только активных пользователей")):
    """Показать список пользователей."""
    async def _list_users():
        user_management = await get_user_management()
        users = await user_management.list_active() if active_only else await user_management.list_all()
        
        if not users:
            console.print("[yellow]Пользователи не найдены[/yellow]")
            return
        
        table = Table(title="Users List")
        for key in format_user(users[0]).keys():
            table.add_column(key)
        
        for user in users:
            table.add_row(*[str(value) for value in format_user(user).values()])
        
        console.print(table)
    
    asyncio.run(_list_users())


@app.command("get")
def get_user(
    user_id: Optional[int] = typer.Option(None, "--id", "-i", help="ID пользователя"),
    telegram_id: Optional[int] = typer.Option(None, "--telegram-id", "-t", help="Telegram ID пользователя"),
):
    """Получить информацию о пользователе."""
    if not user_id and not telegram_id:
        console.print("[red]Необходимо указать либо --id, либо --telegram-id[/red]")
        return
    
    async def _get_user():
        user_management = await get_user_management()
        user = None
        
        if user_id:
            user = await user_management.get_user(user_id)
        elif telegram_id:
            user = await user_management.get_user_by_telegram_id(telegram_id)
        
        if not user:
            console.print("[red]Пользователь не найден[/red]")
            return
        
        table = Table(title="User Info")
        for key, value in format_user(user).items():
            table.add_row(key, str(value))
        
        console.print(table)
    
    asyncio.run(_get_user())


@app.command("create")
def create_user(
    telegram_id: int = typer.Option(..., "--telegram-id", "-t", help="Telegram ID пользователя"),
    username: Optional[str] = typer.Option(None, "--username", "-u", help="Имя пользователя в Telegram"),
    first_name: Optional[str] = typer.Option(None, "--first-name", "-f", help="Имя пользователя"),
    last_name: Optional[str] = typer.Option(None, "--last-name", "-l", help="Фамилия пользователя"),
):
    """Создать нового пользователя."""
    async def _create_user():
        user_management = await get_user_management()
        user = await user_management.create_user(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        
        console.print("[green]Пользователь успешно создан:[/green]")
        table = Table()
        for key, value in format_user(user).items():
            table.add_row(key, str(value))
        console.print(table)
    
    asyncio.run(_create_user())


@app.command("update")
def update_user(
    user_id: int = typer.Option(..., "--id", "-i", help="ID пользователя"),
    username: Optional[str] = typer.Option(None, "--username", "-u", help="Имя пользователя в Telegram"),
    first_name: Optional[str] = typer.Option(None, "--first-name", "-f", help="Имя пользователя"),
    last_name: Optional[str] = typer.Option(None, "--last-name", "-l", help="Фамилия пользователя"),
    active: Optional[bool] = typer.Option(None, "--active/--inactive", help="Активен ли пользователь"),
    admin: Optional[bool] = typer.Option(None, "--admin/--no-admin", help="Является ли пользователь администратором"),
):
    """Обновить информацию о пользователе."""
    async def _update_user():
        user_management = await get_user_management()
        user = await user_management.get_user(user_id)
        
        if not user:
            console.print("[red]Пользователь не найден[/red]")
            return
        
        # Обновляем только переданные поля
        if username is not None:
            user.username = username
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if active is not None:
            user.is_active = active
        if admin is not None:
            user.is_admin = admin
        
        updated_user = await user_management.update_user(user)
        
        console.print("[green]Пользователь успешно обновлен:[/green]")
        table = Table()
        for key, value in format_user(updated_user).items():
            table.add_row(key, str(value))
        console.print(table)
    
    asyncio.run(_update_user())


@app.command("delete")
def delete_user(
    user_id: int = typer.Option(..., "--id", "-i", help="ID пользователя"),
    force: bool = typer.Option(False, "--force", "-f", help="Подтвердить удаление без запроса"),
):
    """Удалить пользователя."""
    if not force:
        if not typer.confirm(f"Вы уверены, что хотите удалить пользователя с ID {user_id}?"):
            return
    
    async def _delete_user():
        user_management = await get_user_management()
        user = await user_management.get_user(user_id)
        
        if not user:
            console.print("[red]Пользователь не найден[/red]")
            return
        
        await user_management.delete_user(user_id)
        console.print(f"[green]Пользователь с ID {user_id} успешно удален[/green]")
    
    asyncio.run(_delete_user()) 